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

    template <typename T>
    using WithNoAnnot = T;

    template <typename T>
    using WithAnnot1 = Fruit::Annotated<Annotation1, T>;
    '''

class TestRegisterProvider(parameterized.TestCase):
    @multiple_parameters([
        'WithNoAnnot',
        'WithAnnot1',
    ], [
       ('X()', 'X'),
       ('new X()', 'X*'),
    ])
    def test_register_provider_success(self, WithAnnot, ConstructX, XPtr):
        source = '''
            struct X : public ConstructionTracker<X> {
              int value = 5;
            };
    
            Fruit::Component<WithAnnot<X>> getComponent() {
              return Fruit::createComponent()
                .registerProvider<WithAnnot<XPtr>()>([](){return ConstructX;});
            }
    
            int main() {
              Fruit::Injector<WithAnnot<X>> injector(getComponent);
    
              Assert((injector.get<WithAnnot<X                 >>(). value == 5));
              Assert((injector.get<WithAnnot<X*                >>()->value == 5));
              Assert((injector.get<WithAnnot<X&                >>(). value == 5));
              Assert((injector.get<WithAnnot<const X           >>(). value == 5));
              Assert((injector.get<WithAnnot<const X*          >>()->value == 5));
              Assert((injector.get<WithAnnot<const X&          >>(). value == 5));
              Assert((injector.get<WithAnnot<std::shared_ptr<X>>>()->value == 5));
        
              Assert(X::num_objects_constructed == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'WithNoAnnot',
        'WithAnnot1',
    ])
    def test_register_provider_abstract_class_ok(self, WithAnnot):
        source = '''
            struct I {
              virtual int foo() = 0;
              virtual ~I() = default;
            };
            
            struct X : public I {
              int foo() override {
                return 5;
              }
            };
    
            Fruit::Component<WithAnnot<I>> getComponent() {
              return Fruit::createComponent()
                .registerProvider<WithAnnot<I*>()>([](){return static_cast<I*>(new X());});
            }
    
            int main() {
              Fruit::Injector<WithAnnot<I>> injector(getComponent);
    
              Assert(injector.get<WithAnnot<I*>>()->foo() == 5);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'WithNoAnnot',
        'WithAnnot1',
    ])
    def test_register_provider_abstract_class_with_no_virtual_destructor_error(self, WithAnnot):
        source = '''
            struct I {
              virtual int foo() = 0;
            };
            
            struct X : public I {
              int foo() override {
                return 5;
              }
            };
    
            Fruit::Component<WithAnnot<I>> getComponent() {
              return Fruit::createComponent()
                .registerProvider<WithAnnot<I*>()>([](){return static_cast<I*>(new X());});
            }
            '''
        expect_compile_error(
            r'ProviderReturningPointerToAbstractClassWithNoVirtualDestructorError<I>',
            r'registerProvider\(\) was called with a lambda that returns a pointer to T, but T is an abstract class',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X()',
        'new X()',
    ])
    def test_register_provider_not_copyable_success(self, ConstructX):
        source = '''
            struct X {
              X() = default;
              X(X&&) = default;
              X(const X&) = delete;
            };
    
            Fruit::Component<X> getComponent() {
              return Fruit::createComponent()
                .registerProvider([](){return ConstructX;});
            }
    
            int main() {
              Fruit::Injector<X> injector(getComponent);
              injector.get<X*>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_provider_not_movable_returning_pointer_success(self):
        source = '''
            struct X {
              X() = default;
              X(X&&) = delete;
              X(const X&) = delete;
            };
    
            Fruit::Component<X> getComponent() {
              return Fruit::createComponent()
                .registerProvider([](){return new X();});
            }
    
            int main() {
              Fruit::Injector<X> injector(getComponent);
              injector.get<X*>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        'X',
        'Fruit::Annotated<Annotation1, X>',
    ])
    def test_register_provider_error_not_function(self, XAnnot):
        source = '''
            struct X {
              X(int) {}
            };
    
            Fruit::Component<XAnnot> getComponent() {
              int n = 3;
              return Fruit::createComponent()
                .registerProvider<XAnnot()>([=]{return X(n);});
            }
            '''
        expect_compile_error(
            'FunctorUsedAsProviderError<.*>',
            'A stateful lambda or a non-lambda functor was used as provider',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'int',
        'Fruit::Annotated<Annotation1, int>',
    ])
    def test_register_provider_error_malformed_signature(self, intAnnot):
        source = '''
            Fruit::Component<intAnnot> getComponent() {
              return Fruit::createComponent()
                .registerProvider<intAnnot>([](){return 42;});
            }
            '''
        expect_compile_error(
            'NotASignatureError<intAnnot>',
            'CandidateSignature was specified as parameter, but it.s not a signature. Signatures are of the form',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X*', '(struct )?X'),
        ('Fruit::Annotated<Annotation1, X>', 'Fruit::Annotated<Annotation1, X*>', '(struct )?Fruit::Annotated<(struct )?Annotation1, ?(struct )?X>'),
    ])
    def test_register_provider_error_returned_nullptr(self, XAnnot, XPtrAnnot, XAnnotRegex):
        source = '''
            struct X {};
    
            Fruit::Component<XAnnot> getComponent() {
              return Fruit::createComponent()
                  .registerProvider<XPtrAnnot()>([](){return (X*)nullptr;});
            }
    
            int main() {
              Fruit::Injector<XAnnot> injector(getComponent);
              injector.get<XAnnot>();
            }
            '''
        expect_runtime_error(
            'Fatal injection error: attempting to get an instance for the type XAnnotRegex but the provider returned nullptr',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('new X()', 'X*'),
    ], [
        'WithNoAnnot',
        'WithAnnot1',
    ], [
        'Y',
        'const Y',
        'Y*',
        'const Y*',
        'Y&',
        'const Y&',
        'std::shared_ptr<Y>',
        'Fruit::Provider<Y>',
        'Fruit::Provider<const Y>',
    ])
    def test_register_provider_with_param_success(self, ConstructX, XPtr, WithAnnot, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            Fruit::Component<WithAnnot<Y>> getYComponent() {
              return Fruit::createComponent()
                .registerConstructor<WithAnnot<Y>()>();
            }
    
            Fruit::Component<X> getComponent() {
              return Fruit::createComponent()
                .install(getYComponent)
                .registerProvider<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; });
            }
    
            int main() {
              Fruit::Injector<X> injector(getComponent);
              injector.get<X>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('new X()', 'X*'),
    ], [
        'WithNoAnnot',
        'WithAnnot1',
    ], [
        'Y',
        'const Y',
        'const Y*',
        'const Y&',
        'Fruit::Provider<const Y>',
    ])
    def test_register_provider_with_param_const_binding_success(self, ConstructX, XPtr, WithAnnot, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            const Y y{};
            
            Fruit::Component<WithAnnot<const Y>> getYComponent() {
              return Fruit::createComponent()
                .bindInstance<WithAnnot<Y>, Y>(y);
            }
    
            Fruit::Component<X> getComponent() {
              return Fruit::createComponent()
                .install(getYComponent)
                .registerProvider<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; });
            }
    
            int main() {
              Fruit::Injector<X> injector(getComponent);
              injector.get<X>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('new X()', 'X*'),
    ], [
        ('WithNoAnnot', 'Y'),
        ('WithAnnot1', 'Fruit::Annotated<Annotation1, Y>'),
    ], [
        'Y*',
        'Y&',
        'std::shared_ptr<Y>',
        'Fruit::Provider<Y>',
    ])
    def test_register_provider_with_param_error_nonconst_param_required(self, ConstructX, XPtr, WithAnnot, YAnnotRegex, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            Fruit::Component<WithAnnot<const Y>> getYComponent();
    
            Fruit::Component<> getComponent() {
              return Fruit::createComponent()
                .install(getYComponent)
                .registerProvider<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; });
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<YAnnotRegex>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('new X()', 'X*'),
    ], [
        ('WithNoAnnot', 'Y'),
        ('WithAnnot1', 'Fruit::Annotated<Annotation1, Y>'),
    ], [
        'Y*',
        'Y&',
        'std::shared_ptr<Y>',
        'Fruit::Provider<Y>',
    ])
    def test_register_provider_with_param_error_nonconst_param_required_install_after(self, ConstructX, XPtr, WithAnnot, YAnnotRegex, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            Fruit::Component<WithAnnot<const Y>> getYComponent();
    
            Fruit::Component<> getComponent() {
              return Fruit::createComponent()
                .registerProvider<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; })
                .install(getYComponent);
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<YAnnotRegex>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_provider_requiring_nonconst_then_requiring_const_ok(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Fruit::Component<Y, Z> getRootComponent() {
              return Fruit::createComponent()
                .registerProvider([](X&) { return Y();})
                .registerProvider([](const X&) { return Z();})
                .registerConstructor<X()>();
            }
            
            int main() {
              Fruit::Injector<Y, Z> injector(getRootComponent);
              injector.get<Y>();
              injector.get<Z>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_provider_requiring_nonconst_then_requiring_const_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Fruit::Component<Fruit::Required<const X>, Y, Z> getRootComponent() {
              return Fruit::createComponent()
                .registerProvider([](X&) { return Y();})
                .registerProvider([](const X&) { return Z();});
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_provider_requiring_const_then_requiring_nonconst_ok(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Fruit::Component<Y, Z> getRootComponent() {
              return Fruit::createComponent()
                .registerProvider([](const X&) { return Y();})
                .registerProvider([](X&) { return Z();})
                .registerConstructor<X()>();
            }
            
            int main() {
              Fruit::Injector<Y, Z> injector(getRootComponent);
              injector.get<Y>();
              injector.get<Z>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_provider_requiring_const_then_requiring_nonconst_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Fruit::Component<Fruit::Required<const X>, Y, Z> getRootComponent() {
              return Fruit::createComponent()
                .registerProvider([](const X&) { return Y();})
                .registerProvider([](X&) { return Z();});
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('new X()', 'X*'),
    ], [
        ('Y**', r'Y\*\*'),
        ('std::shared_ptr<Y>*', r'std::shared_ptr<Y>\*'),
        ('std::nullptr_t', r'(std::)?nullptr(_t)?'),
        ('Y*&', r'Y\*&'),
        ('Y(*)()', r'Y(\((__cdecl)?\*\))?\((void)?\)'),
    ])
    def test_register_provider_with_param_error_type_not_injectable(self, ConstructX, XPtr, YVariant, YVariantRegex):
        source = '''
            struct Y {};
            struct X {};
            
            Fruit::Component<> getComponent() {
              return Fruit::createComponent()
                .registerProvider<XPtr(YVariant)>([](YVariant){ return ConstructX; });
            }
            '''
        expect_compile_error(
            'NonInjectableTypeError<YVariantRegex>',
            'The type T is not injectable.',
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
