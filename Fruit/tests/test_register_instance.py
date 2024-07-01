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
    
    struct Annotation1 {};
    '''

def escape_regex(regex):
    # We un-escape the space because we strip the spaces in fruit_test_common, and this would otherwise leave a
    # stray backslash.
    return re.escape(regex).replace('\\ ', ' ')

class TestRegisterInstance(parameterized.TestCase):
    def test_bind_instance_success(self):
        source = '''
            struct X {
              int n;
    
              X(int n)
                : n(n) {
              }
            };
    
            Poco::Fruit::Component<X> getComponent(X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance(*x);
            }
    
            int main() {
              X x(34);
              Poco::Fruit::Injector<X> injector(getComponent, &x);
              X& x1 = injector.get<X&>();
              Assert(&x == &x1);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_bind_instance_annotated_success(self):
        source = '''
            struct X {
              int n;
    
              X(int n)
                : n(n) {
              }
            };
    
            Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation1, X>> getComponent(X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance<Poco::Fruit::Annotated<Annotation1, X>>(*x);
            }
    
            int main() {
              X x(34);
              Poco::Fruit::Injector<Poco::Fruit::Annotated<Annotation1, X>> injector(getComponent, &x);
              X& x1 = injector.get<Poco::Fruit::Annotated<Annotation1, X&>>();
              Assert(&x == &x1);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_bind_const_instance_success(self):
        source = '''
            struct X {
              int n;
    
              X(int n)
                : n(n) {
              }
            };
    
            Poco::Fruit::Component<const X> getComponent(const X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance(*x);
            }
    
            const X x(34);
            
            int main() {
              Poco::Fruit::Injector<const X> injector(getComponent, &x);
              const X& x1 = injector.get<const X&>();
              Assert(&x == &x1);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_bind_const_instance_annotated_success(self):
        source = '''
            struct X {
              int n;
    
              X(int n)
                : n(n) {
              }
            };
    
            Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation1, const X>> getComponent(const X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance<Poco::Fruit::Annotated<Annotation1, X>>(*x);
            }
    
            const X x(34);
            
            int main() {
              Poco::Fruit::Injector<Poco::Fruit::Annotated<Annotation1, const X>> injector(getComponent, &x);
              const X& x1 = injector.get<Poco::Fruit::Annotated<Annotation1, const X&>>();
              Assert(&x == &x1);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    @parameterized.parameters([
        ('X', 'X', 'X*', 'X*'),
        ('X', 'const X', 'const X*', 'const X*'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, X>', 'X*', 'Poco::Fruit::Annotated<Annotation1, X*>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X>', 'const X*', 'Poco::Fruit::Annotated<Annotation1, const X*>'),
    ])
    def test_bind_instance_two_explicit_type_arguments_success(self, XAnnot, MaybeConstXAnnot, XPtr, XPtrAnnot):
        source = '''
            struct X {
              int n;
    
              X(int n)
                : n(n) {
              }
            };
    
            Poco::Fruit::Component<MaybeConstXAnnot> getComponent(XPtr x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XAnnot, X>(*x);
            }
    
            int main() {
              X x(34);
              Poco::Fruit::Injector<MaybeConstXAnnot> injector(getComponent, &x);
              XPtr x1 = injector.get<XPtrAnnot>();
              Assert(&x == x1);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source, locals())

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_bind_instance_abstract_class_ok(self, XAnnot):
        source = '''
            struct X {
              virtual void foo() = 0;
            };
            
            Poco::Fruit::Component<> getComponentForInstanceHelper(X* x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XAnnot, X>(*x);
            }
    
            Poco::Fruit::Component<XAnnot> getComponentForInstance(X* x) {
              return Poco::Fruit::createComponent()
                .install(getComponentForInstanceHelper, x)
                .bindInstance<XAnnot, X>(*x);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('int', 'int*'),
        ('Poco::Fruit::Annotated<Annotation1, int>', 'Poco::Fruit::Annotated<Annotation1, int*>'),
    ])
    def test_bind_instance_multiple_equivalent_bindings_success(self, intAnnot, intPtrAnnot):
        source = '''
            Poco::Fruit::Component<> getComponentForInstanceHelper(int* n) {
              return Poco::Fruit::createComponent()
                .bindInstance<intAnnot, int>(*n);
            }
            
            Poco::Fruit::Component<intAnnot> getComponentForInstance(int* n) {
              return Poco::Fruit::createComponent()
                .install(getComponentForInstanceHelper, n)
                .bindInstance<intAnnot, int>(*n);
            }
    
            int main() {
              int n = 5;
              Poco::Fruit::Injector<intAnnot> injector(getComponentForInstance, &n);
              if (injector.get<intPtrAnnot>() != &n)
                abort();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('int', 'int*'),
        ('Poco::Fruit::Annotated<Annotation1, int>', 'Poco::Fruit::Annotated<Annotation1, int*>'),
    ])
    def test_bind_instance_multiple_equivalent_bindings_different_constness_success(self, intAnnot, intPtrAnnot):
        source = '''
            Poco::Fruit::Component<> getComponentForInstanceHelper(const int* n) {
              return Poco::Fruit::createComponent()
                .bindInstance<intAnnot, int>(*n);
            }
            
            Poco::Fruit::Component<intAnnot> getComponentForInstance(int* n) {
              return Poco::Fruit::createComponent()
                .install(getComponentForInstanceHelper, n)
                .bindInstance<intAnnot, int>(*n);
            }
    
            int main() {
              int n = 5;
              Poco::Fruit::Injector<intAnnot> injector(getComponentForInstance, &n);
              if (injector.get<intPtrAnnot>() != &n)
                abort();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('int', 'int*'),
        ('Poco::Fruit::Annotated<Annotation1, int>', 'Poco::Fruit::Annotated<Annotation1, int*>'),
    ])
    def test_bind_instance_multiple_equivalent_bindings_different_constness_other_order_success(self, intAnnot, intPtrAnnot):
        source = '''
            Poco::Fruit::Component<> getComponentForInstanceHelper(const int* n) {
              return Poco::Fruit::createComponent()
                .bindInstance<intAnnot, int>(*n);
            }
            
            Poco::Fruit::Component<intAnnot> getComponentForInstance(int* n) {
              return Poco::Fruit::createComponent()
                .bindInstance<intAnnot, int>(*n)
                .install(getComponentForInstanceHelper, n);
            }
    
            int main() {
              int n = 5;
              Poco::Fruit::Injector<intAnnot> injector(getComponentForInstance, &n);
              if (injector.get<intPtrAnnot>() != &n)
                abort();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X*',
        'const X*',
        'std::shared_ptr<X>',
    ])
    def test_bind_instance_non_normalized_type_error(self, XVariant):
        if XVariant.endswith('&'):
            XVariantRegexp = escape_regex(XVariant[:-1])
        else:
            XVariantRegexp = escape_regex(XVariant)
        source = '''
            struct X {};
    
            Poco::Fruit::Component<> getComponent(XVariant x) {
              return Poco::Fruit::createComponent()
                .bindInstance(x);
            }
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegexp,X>',
            'A non-class type T was specified. Use C instead.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', r'const X'),
        ('X*', r'X\*'),
        ('const X*', r'const X\*'),
        ('X&', r'X&'),
        ('const X&', r'const X&'),
        ('std::shared_ptr<X>', r'std::shared_ptr<X>'),
    ])
    def test_bind_instance_non_normalized_type_error_with_annotation(self, XVariant, XVariantRegexp):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<> getComponent(XVariant x) {
              return Poco::Fruit::createComponent()
                .bindInstance<Poco::Fruit::Annotated<Annotation1, XVariant>>(x);
            }
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegexp,X>',
            'A non-class type T was specified. Use C instead.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', 'const X'),
        ('X*', 'X*'),
        ('const X*', 'const X*'),
        ('X&', 'X&'),
        ('const X&', 'const X&'),
        ('std::shared_ptr<X>', 'std::shared_ptr<X>'),

        ('Poco::Fruit::Annotated<Annotation1, const X>', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X*>', 'X*'),
        ('Poco::Fruit::Annotated<Annotation1, const X*>', 'const X*'),
        ('Poco::Fruit::Annotated<Annotation1, X&>', 'X&'),
        ('Poco::Fruit::Annotated<Annotation1, const X&>', 'const X&'),
        ('Poco::Fruit::Annotated<Annotation1, std::shared_ptr<X>>', 'std::shared_ptr<X>'),

        ('Poco::Fruit::Annotated<Annotation1, X>', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'X*'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'const X*'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'X&'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'const X&'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'std::shared_ptr<X>'),
    ])
    def test_bind_instance_non_normalized_type_error_two_explicit_type_arguments(self, XAnnotVariant, XVariant):
        XVariantRegexp = escape_regex(XVariant)
        source = '''
            struct X {};
    
            Poco::Fruit::Component<> getComponent(XVariant x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XAnnotVariant, XVariant>(x);
            }
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegexp,X>',
            'A non-class type T was specified. Use C instead.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X*', r'X\*'),
        ('const X*', r'const X\*'),
        ('std::shared_ptr<X>', r'std::shared_ptr<X>'),
    ])
    def test_register_instance_error_must_be_reference(self, XVariant, XVariantRegex):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<> getComponentForInstance(XVariant x) {
              return Poco::Fruit::createComponent()
                  .bindInstance(x);
            }
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegex,X>',
            'A non-class type T was specified. Use C instead.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X*', r'X\*'),
        ('const X*', r'const X\*'),
        ('std::shared_ptr<X>', r'std::shared_ptr<X>'),
    ])
    def test_register_instance_error_must_be_reference_with_annotation(self, XVariant, XVariantRegex):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<> getComponentForInstance(XVariant x) {
              return Poco::Fruit::createComponent()
                  .bindInstance<Poco::Fruit::Annotated<Annotation1, X>>(x);
            }
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegex,X>',
            'A non-class type T was specified. Use C instead.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_bind_instance_mismatched_type_arguments(self, XAnnot):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<> getComponent(int* n) {
              return Poco::Fruit::createComponent()
                .bindInstance<XAnnot, int>(*n);
            }
            '''
        expect_compile_error(
            'TypeMismatchInBindInstanceError<X,int>',
            'A type parameter was specified in bindInstance.. but it doesn.t match the value type',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Base', 'Base*'),
        ('Poco::Fruit::Annotated<Annotation1, Base>', 'Poco::Fruit::Annotated<Annotation1, Base*>'),
    ])
    def test_bind_instance_to_subclass(self, BaseAnnot, BasePtrAnnot):
        source = '''
            struct Base {
              virtual void f() = 0;
              virtual ~Base() {
              }
            };
    
            struct Derived : public Base {
              void f() override {
              }
            };
    
            Poco::Fruit::Component<BaseAnnot> getComponent(Derived* derived) {
              return Poco::Fruit::createComponent()
                .bindInstance<BaseAnnot, Base>(*derived);
            }
    
            int main() {
              Derived derived;
              Poco::Fruit::Injector<BaseAnnot> injector(getComponent, &derived);
              Base* base = injector.get<BasePtrAnnot>();
              base->f();
            }
            '''
        expect_success(COMMON_DEFINITIONS, source, locals())

    @parameterized.parameters([
        ('X**', r'X\*\*'),
        ('std::shared_ptr<X>*', r'std::shared_ptr<X>\*'),
        ('X*&', r'X\*&'),
        ('Poco::Fruit::Annotated<Annotation1, X**>', r'X\*\*'),
    ])
    def test_bind_instance_type_not_normalized(self, XVariant, XVariantRegex):
        source = '''
            struct X {};
    
            using XVariantT = XVariant;
            Poco::Fruit::Component<> getComponent(XVariantT x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XVariant, XVariant>(x);
            }
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegex,X>',
            'A non-class type T was specified.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X(*)()', r'X(\((__cdecl)?\*\))?\((void)?\)'),
    ])
    def test_bind_instance_type_not_injectable_error(self, XVariant, XVariantRegex):
        source = '''
            struct X {};
            
            using XVariantT = XVariant;
            Poco::Fruit::Component<> getComponent(XVariantT x) {
              return Poco::Fruit::createComponent()
                .bindInstance<XVariant, XVariant>(x);
            }
            '''
        expect_compile_error(
            'NonInjectableTypeError<XVariantRegex>',
            'The type T is not injectable.',
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
