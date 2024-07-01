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
    using XAnnot = Poco::Fruit::Annotated<Annotation1, X>;

    struct Annotation2 {};
    '''

class TestInjectedProvider(parameterized.TestCase):
    @parameterized.parameters([
        ('X*', r'X\*'),
        ('const X*', r'const X\*'),
        ('X&', r'X&'),
        ('const X&', r'const X&'),
        ('std::shared_ptr<X>', r'std::shared_ptr<X>'),
    ])
    def test_error_non_class_type_parameter(self, XVariant, XVariantRegexp):
        source = '''
            struct X {};
    
            Poco::Fruit::Provider<XVariant> provider;
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegexp,X>',
            'A non-class type T was specified. Use C instead',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_error_annotated_type_parameter(self):
        source = '''
            struct X {};
    
            Poco::Fruit::Provider<XAnnot> provider;
            '''
        expect_compile_error(
            'AnnotatedTypeError<Poco::Fruit::Annotated<Annotation1,X>,X>',
            'An annotated type was specified where a non-annotated type was expected.',
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'X'),
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'const X&'),
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'const X*'),
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'X&'),
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'X*'),
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'std::shared_ptr<X>'),
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'Poco::Fruit::Provider<X>'),
        ('X', 'Poco::Fruit::Provider<X>', 'X', 'Poco::Fruit::Provider<const X>'),
        ('X', 'Poco::Fruit::Provider<const X>', 'const X', 'const X&'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, Poco::Fruit::Provider<X>>', 'X', 'const X&'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, Poco::Fruit::Provider<const X>>', 'const X', 'const X&'),
    ])
    def test_provider_get_ok(self, XBindingInInjector, XProviderAnnot, XParamInProvider, XProviderGetParam):
        source = '''
            struct X {
              using Inject = X();
            };
    
            Poco::Fruit::Component<XBindingInInjector> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<XBindingInInjector> injector(getComponent);
              Poco::Fruit::Provider<XParamInProvider> provider = injector.get<XProviderAnnot>();
    
              XProviderGetParam x = provider.get<XProviderGetParam>();
              (void)x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', 'Poco::Fruit::Provider<const X>', 'const X', 'X'),
        ('const X', 'Poco::Fruit::Provider<const X>', 'const X', 'const X&'),
        ('const X', 'Poco::Fruit::Provider<const X>', 'const X', 'const X*'),
        ('const X', 'Poco::Fruit::Provider<const X>', 'const X', 'Poco::Fruit::Provider<const X>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, Poco::Fruit::Provider<const X>>', 'const X', 'const X&'),
    ])
    def test_provider_get_const_binding_ok(self, XBindingInInjector, XProviderAnnot, XParamInProvider, XProviderGetParam):
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
              Poco::Fruit::Provider<XParamInProvider> provider = injector.get<XProviderAnnot>();
    
              XProviderGetParam x = provider.get<XProviderGetParam>();
              (void)x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_provider_get_during_injection_ok(self):
        source = '''
            struct X {
              INJECT(X()) = default;
              void foo() {
              }
            };
    
            struct Y {
              X x;
              INJECT(Y(Poco::Fruit::Provider<X> xProvider))
                : x(xProvider.get<X>()) {
              }
    
              void foo() {
                x.foo();
              }
            };
    
            struct Z {
              Y y;
              INJECT(Z(Poco::Fruit::Provider<Y> yProvider))
                  : y(yProvider.get<Y>()) {
              }
    
              void foo() {
                y.foo();
              }
            };
    
            Poco::Fruit::Component<Z> getZComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<Z> injector(getZComponent);
              Poco::Fruit::Provider<Z> provider(injector);
              // During provider.get<Z>(), yProvider.get() is called, and during that xProvider.get()
              // is called.
              Z z = provider.get<Z>();
              z.foo();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_provider_get_error_type_not_provided(self):
        source = '''
            struct X {};
            struct Y {};
    
            void f(Poco::Fruit::Provider<X> provider) {
              provider.get<Y>();
            }
            '''
        expect_compile_error(
            'TypeNotProvidedError<Y>',
            'Trying to get an instance of T, but it is not provided by this Provider/Injector.',
            COMMON_DEFINITIONS,
            source)

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
        ('Poco::Fruit::Annotated<Annotation1, Poco::Fruit::Annotated<Annotation1, X>>', r'Poco::Fruit::Annotated<Annotation1, X>'),
    ])
    def test_provider_get_error_type_not_injectable(self, XVariant, XVariantRegex):
        source = '''
            struct X {};
    
            void f(Poco::Fruit::Provider<X> provider) {
              provider.get<XVariant>();
            }
            '''
        expect_compile_error(
            'NonInjectableTypeError<XVariantRegex>',
            'The type T is not injectable',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X&', r'X&'),
        ('X*', r'X\*'),
        ('std::shared_ptr<X>', r'std::shared_ptr<X>'),
        ('Poco::Fruit::Provider<X>', r'Poco::Fruit::Provider<X>'),
    ])
    def test_const_provider_get_does_not_allow_injecting_nonconst_variants(self, XProviderGetParam, XProviderGetParamRegex):
        source = '''
            void f(Poco::Fruit::Provider<const X> provider) {
              provider.get<XProviderGetParam>();
            }
            '''
        expect_compile_error(
            'TypeProvidedAsConstOnlyError<XProviderGetParamRegex>',
            'Trying to get an instance of T, but it is only provided as a constant by this Provider/Injector',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Poco::Fruit::Provider<Y>'),
        ('ANNOTATED(Annotation1, Poco::Fruit::Provider<Y>)'),
    ])
    def test_lazy_injection_with_annotations(self, Y_PROVIDER_ANNOT):
        source = '''
            struct Y : public ConstructionTracker<Y> {
              using Inject = Y();
            };
    
            struct X : public ConstructionTracker<X> {
              INJECT(X(Y_PROVIDER_ANNOT provider)) : provider(provider) {
              }
    
              void run() {
                Y* y(provider);
                (void) y;
              }
    
              Poco::Fruit::Provider<Y> provider;
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent();
            }
            
            Poco::Fruit::Component<> getEmptyComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<> normalizedComponent(getEmptyComponent);
              Poco::Fruit::Injector<X> injector(normalizedComponent, getComponent);
    
              Assert(X::num_objects_constructed == 0);
              Assert(Y::num_objects_constructed == 0);
    
              X* x(injector);
    
              Assert(X::num_objects_constructed == 1);
              Assert(Y::num_objects_constructed == 0);
    
              x->run();
    
              Assert(X::num_objects_constructed == 1);
              Assert(Y::num_objects_constructed == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
