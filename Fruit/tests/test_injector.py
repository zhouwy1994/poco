#!/usr/bin/env python3
#  Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from absl.testing import parameterized
from fruit_test_common import *

COMMON_DEFINITIONS = '''
    #include "test_common.h"

    struct X;

    struct Annotation1 {};
    using XAnnot1 = Poco::Fruit::Annotated<Annotation1, X>;

    struct Annotation2 {};
    using XAnnot2 = Poco::Fruit::Annotated<Annotation2, X>;
    '''

class TestInjector(parameterized.TestCase):
    def test_empty_injector(self):
        source = '''
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getComponent);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_error_component_with_requirements(self, XAnnot):
        source = '''
            struct X {};
        
            Poco::Fruit::Component<Poco::Fruit::Required<XAnnot>> getComponent();
    
            void f(Poco::Fruit::NormalizedComponent<XAnnot> normalizedComponent) {
              Poco::Fruit::Injector<XAnnot> injector(normalizedComponent, getComponent);
            }
            '''
        expect_compile_error(
            'ComponentWithRequirementsInInjectorError<XAnnot>',
            'When using the two-argument constructor of Injector, the component used as second parameter must not have requirements',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_error_declared_types_not_provided(self, XAnnot):
        source = '''
            struct X {
              using Inject = X();
            };
            
            Poco::Fruit::Component<> getEmptyComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<> normalizedComponent(getEmptyComponent);
              Poco::Fruit::Injector<XAnnot> injector(normalizedComponent, getEmptyComponent);
            }
            '''
        expect_compile_error(
            'TypesInInjectorNotProvidedError<XAnnot>',
            'The types in TypesNotProvided are declared as provided by the injector, but none of the two components passed to the Injector constructor provides them.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_error_declared_nonconst_types_provided_as_const(self, XAnnot, ConstXAnnot):
        source = '''
            struct X {
              using Inject = X();
            };
            
            Poco::Fruit::Component<ConstXAnnot> getComponent();
    
            int main() {
              Poco::Fruit::Injector<XAnnot> injector(getComponent);
            }
            '''
        expect_generic_compile_error(
            r'no matching constructor for initialization of .Poco::Fruit::Injector<XAnnot>.'
            r'|no matching function for call to .Poco::Fruit::Injector<XAnnot>::Injector\(Poco::Fruit::Component<ConstXAnnot> \(&\)\(\)\).'
            # MSVC
            r'|.Poco::Fruit::Injector<XAnnot>::Injector.: no overloaded function could convert all the argument types'
            r'|.Poco::Fruit::Injector<XAnnot>::Injector.: none of the 2 overloads could convert all the argument types',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_error_declared_nonconst_types_provided_as_const_with_normalized_component(self, XAnnot, ConstXAnnot):
        source = '''
            struct X {};
            
            Poco::Fruit::Component<> getEmptyComponent();
            
            void f(Poco::Fruit::NormalizedComponent<ConstXAnnot> normalizedComponent) {
              Poco::Fruit::Injector<XAnnot> injector(normalizedComponent, getEmptyComponent);
            }
            '''
        expect_compile_error(
            'TypesInInjectorProvidedAsConstOnlyError<XAnnot>',
            'The types in TypesProvidedAsConstOnly are declared as non-const provided types by the injector',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'Y'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation2, Y>'),
    ])
    def test_injector_get_error_type_not_provided(self, XAnnot, YAnnot):
        source = '''
            struct X {
              using Inject = X();
            };
    
            struct Y {};
    
            Poco::Fruit::Component<XAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<XAnnot> injector(getComponent);
              injector.get<YAnnot>();
            }
            '''
        expect_compile_error(
            'TypeNotProvidedError<YAnnot>',
            'Trying to get an instance of T, but it is not provided by this Provider/Injector.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', 'X&', r'X&'),
        ('const X', 'X*', r'X\*'),
        ('const X', 'std::shared_ptr<X>', r'std::shared_ptr<X>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, X&>', r'Poco::Fruit::Annotated<Annotation1, X&>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, X*>', r'Poco::Fruit::Annotated<Annotation1, X\*>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, std::shared_ptr<X>>', r'Poco::Fruit::Annotated<Annotation1, std::shared_ptr<X>>'),
    ])
    def test_injector_const_provided_type_does_not_allow_injecting_nonconst_variants(self, ConstXAnnot, XInjectorGetParam, XInjectorGetParamRegex):
        source = '''
            void f(Poco::Fruit::Injector<ConstXAnnot> injector) {
              injector.get<XInjectorGetParam>();
            }
            '''
        expect_compile_error(
            'TypeProvidedAsConstOnlyError<XInjectorGetParamRegex>',
            'Trying to get an instance of T, but it is only provided as a constant by this Provider/Injector',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X'),
        ('X', 'const X&'),
        ('X', 'const X*'),
        ('X', 'X&'),
        ('X', 'X*'),
        ('X', 'std::shared_ptr<X>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, X>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X&>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X*>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, X&>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, X*>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, std::shared_ptr<X>>'),
    ])
    def test_injector_get_ok(self, XBindingInInjector, XInjectorGetParam):
        source = '''
            struct X {
              using Inject = X();
            };
    
            Poco::Fruit::Component<XBindingInInjector> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<XBindingInInjector> injector(getComponent);
    
              auto x = injector.get<XInjectorGetParam>();
              (void)x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', 'X'),
        ('const X', 'const X&'),
        ('const X', 'const X*'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, X>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, const X&>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, const X*>'),
    ])
    def test_injector_get_const_binding_ok(self, XBindingInInjector, XInjectorGetParam):
        XBindingInInjectorWithoutConst = XBindingInInjector.replace('const ', '')
        source = '''
            struct X {};
            
            const X x{};
    
            Poco::Fruit::Component<XBindingInInjector> getComponent() {
              return Poco::Fruit::createComponent()
                  .bindInstance<XBindingInInjectorWithoutConst, X>(x);
            }
    
            int main() {
              Poco::Fruit::Injector<XBindingInInjector> injector(getComponent);
    
              auto x = injector.get<XInjectorGetParam>();
              (void)x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X**', r'X\*\*'),
        ('std::shared_ptr<X>*', r'std::shared_ptr<X>\*'),
        ('const std::shared_ptr<X>', r'const std::shared_ptr<X>'),
        ('X* const', r'X\* const'),
        ('const X* const', r'const X\* const'),
        ('std::nullptr_t', r'(std::)?nullptr(_t)?'),
        ('X*&', r'X\*&'),
        ('X(*)()', r'X(\((__cdecl)?\*\))?\((void)?\)'),
        ('void', r'void'),
        ('Poco::Fruit::Annotated<Annotation1, X**>', r'X\*\*'),
    ])
    def test_injector_get_error_type_not_injectable(self, XVariant, XVariantRegex):
        source = '''
            struct X {};
    
            void f(Poco::Fruit::Injector<X> injector) {
              injector.get<XVariant>();
            }
            '''
        expect_compile_error(
            'NonInjectableTypeError<XVariantRegex>',
            'The type T is not injectable.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X[]', r'X\[\]'),
    ])
    def test_injector_get_error_array_type(self, XVariant, XVariantRegex):
        source = '''
            struct X {};
    
            void f(Poco::Fruit::Injector<X> injector) {
              injector.get<XVariant>();
            }
            '''
        expect_generic_compile_error(
            'function cannot return array type'
            '|function returning an array'
            # MSVC
            '|.Poco::Fruit::Injector<X>::get.: no matching overloaded function found',
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
