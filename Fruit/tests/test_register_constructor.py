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

    struct Annotation3 {};
    
    template <typename T>
    using WithNoAnnotation = T;
    
    template <typename T>
    using WithAnnotation1 = Poco::Fruit::Annotated<Annotation1, T>;
    '''

class TestRegisterConstructor(parameterized.TestCase):

    def test_register_constructor_success_copyable_and_movable(self):
        source = '''
            struct X {
              INJECT(X()) = default;
              X(X&&) = default;
              X(const X&) = default;
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getComponent);
              injector.get<X*>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_register_constructor_success_movable_only(self):
        source = '''
            struct X {
              INJECT(X()) = default;
              X(X&&) = default;
              X(const X&) = delete;
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getComponent);
              injector.get<X*>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_register_constructor_success_not_movable(self):
        source = '''
            struct X {
              INJECT(X()) = default;
              X(X&&) = delete;
              X(const X&) = delete;
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getComponent);
              injector.get<X*>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    # TODO: consider moving to test_normalized_component.py
    @parameterized.parameters([
        ('X', 'Y', 'Y', 'Z'),
        ('X', 'Y', 'const Y', 'Z'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation2, Y>', 'Poco::Fruit::Annotated<Annotation2, const Y>', 'Poco::Fruit::Annotated<Annotation3, Z>'),
    ])
    def test_autoinject_with_annotation_success(self, XAnnot, YAnnot, MaybeConstYAnnot, ZAnnot):
        source = '''
            struct X {
              using Inject = X();
            };
    
            struct Y : public ConstructionTracker<Y> {
              using Inject = Y();
            };
    
            struct Z {
              using Inject = Z();
            };
    
            Poco::Fruit::Component<ZAnnot, MaybeConstYAnnot, XAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
            
            Poco::Fruit::Component<> getEmptyComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<> normalizedComponent(getEmptyComponent);
              Poco::Fruit::Injector<MaybeConstYAnnot> injector(normalizedComponent, getComponent);
    
              Assert(Y::num_objects_constructed == 0);
              injector.get<YAnnot>();
              Assert(Y::num_objects_constructed == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_autoinject_annotation_in_signature_return_type(self):
        source = '''
            struct X {
              using Inject = XAnnot();
            };
    
            Poco::Fruit::Component<XAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'InjectTypedefWithAnnotationError<X>',
            'C::Inject is a signature that returns an annotated type',
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_wrong_class_in_typedef(self):
        source = '''
            struct X {
              using Inject = X();
            };
    
            struct Y : public X {
            };
    
            Poco::Fruit::Component<Y> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'InjectTypedefForWrongClassError<Y,X>',
            'C::Inject is a signature, but does not return a C. Maybe the class C has no Inject typedef and',
            COMMON_DEFINITIONS,
            source)

    def test_register_constructor_error_abstract_class(self):
        if re.search('MSVC', CXX_COMPILER_NAME) is not None:
            # MSVC allows to construct the type X(int*) but SignatureType<Type<X(int*)>> doesn't find the
            # specialization.
            return
        source = '''
            struct X {
              X(int*) {}
    
              virtual void foo() = 0;
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<Poco::Fruit::Annotated<Annotation1, X>(int*)>();
            }
            '''
        # Some compilers give a generic compile error, some don't and then Fruit reports the error.
        try:
            expect_generic_compile_error(
                'invalid abstract return type'
                '|.X.: cannot instantiate abstract class',
                COMMON_DEFINITIONS,
                source)
        except:
            expect_compile_error(
                'CannotConstructAbstractClassError<X>',
                'The specified class can.t be constructed because it.s an abstract class',
                COMMON_DEFINITIONS,
                source)

    def test_register_constructor_error_malformed_signature(self):
        source = '''
            struct X {
              X(int) {}
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<X[]>();
            }
            '''
        expect_compile_error(
            r'NotASignatureError<X\[\]>',
            r'CandidateSignature was specified as parameter, but it.s not a signature. Signatures are of the form',
            COMMON_DEFINITIONS,
            source)

    def test_register_constructor_error_malformed_signature_autoinject(self):
        source = '''
            struct X {
              using Inject = X[];
              X(int) {}
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            r'InjectTypedefNotASignatureError<X,X\[\]>',
            r'C::Inject should be a typedef to a signature',
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        'char*',
        'Poco::Fruit::Annotated<Annotation1, char*>',
    ])
    def test_register_constructor_does_not_exist_error(self, charPtrAnnot):
        source = '''
            struct X {
              X(int*) {}
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<X(charPtrAnnot)>();
            }
            '''
        expect_compile_error(
            r'NoConstructorMatchingInjectSignatureError<X,X\(char\*\)>',
            r'contains an Inject typedef but it.s not constructible with the specified types',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'char*',
        'Poco::Fruit::Annotated<Annotation1, char*>',
    ])
    def test_autoinject_constructor_does_not_exist_error(self, charPtrAnnot):
        source = '''
            struct X {
              using Inject = X(charPtrAnnot);
              X(int*) {}
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            r'NoConstructorMatchingInjectSignatureError<X,X\(char\*\)>',
            r'contains an Inject typedef but it.s not constructible with the specified types',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_autoinject_abstract_class_error(self):
        source = '''
            struct X {
              using Inject = Poco::Fruit::Annotated<Annotation1, X>();
    
              virtual void scale() = 0;
              // Note: here we "forgot" to implement scale() (on purpose, for this test) so X is an abstract class.
            };
    
            Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation1, X>> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'CannotConstructAbstractClassError<X>',
            'The specified class can.t be constructed because it.s an abstract class.',
            COMMON_DEFINITIONS,
            source)

    @multiple_parameters([
        'WithNoAnnotation',
        'WithAnnotation1',
    ], [
        'Y',
        'const Y',
        'Y*',
        'const Y*',
        'Y&',
        'const Y&',
        'std::shared_ptr<Y>',
        'Poco::Fruit::Provider<Y>',
        'Poco::Fruit::Provider<const Y>',
    ])
    def test_register_constructor_with_param_success(self, WithAnnotation, YVariant):
        source = '''
            struct Y {};
            struct X {
              X(YVariant) {
              }
            };
            
            Poco::Fruit::Component<WithAnnotation<Y>> getYComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<WithAnnotation<Y>()>();
            }
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getYComponent)
                .registerConstructor<X(WithAnnotation<YVariant>)>();
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getComponent);
              injector.get<X>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        'WithNoAnnotation',
        'WithAnnotation1',
    ], [
        'Y',
        'const Y',
        'const Y*',
        'const Y&',
        'Poco::Fruit::Provider<const Y>',
    ])
    def test_register_constructor_with_param_const_binding_success(self, WithAnnotation, YVariant):
        source = '''
            struct Y {};
            struct X {
              X(YVariant) {
              }
            };
            
            const Y y{};
            
            Poco::Fruit::Component<WithAnnotation<const Y>> getYComponent() {
              return Poco::Fruit::createComponent()
                .bindInstance<WithAnnotation<Y>, Y>(y);
            }
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getYComponent)
                .registerConstructor<X(WithAnnotation<YVariant>)>();
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getComponent);
              injector.get<X>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('WithNoAnnotation', 'Y'),
        ('WithAnnotation1', 'Poco::Fruit::Annotated<Annotation1,Y>'),
    ], [
        'Y*',
        'Y&',
        'std::shared_ptr<Y>',
        'Poco::Fruit::Provider<Y>',
    ])
    def test_register_constructor_with_param_error_nonconst_param_required(self, WithAnnotation, YAnnotRegex, YVariant):
        source = '''
            struct Y {};
            struct X {
              X(YVariant);
            };
            
            Poco::Fruit::Component<WithAnnotation<const Y>> getYComponent();
    
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getYComponent)
                .registerConstructor<X(WithAnnotation<YVariant>)>();
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<YAnnotRegex>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('WithNoAnnotation', 'Y'),
        ('WithAnnotation1', 'Poco::Fruit::Annotated<Annotation1, Y>'),
    ], [
        'Y*',
        'Y&',
        'std::shared_ptr<Y>',
        'Poco::Fruit::Provider<Y>',
    ])
    def test_register_constructor_with_param_error_nonconst_param_required_install_after(self, WithAnnotation, YAnnotRegex, YVariant):
        source = '''
            struct Y {};
            struct X {
              X(YVariant);
            };
            
            Poco::Fruit::Component<WithAnnotation<const Y>> getYComponent();
    
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<X(WithAnnotation<YVariant>)>()
                .install(getYComponent);
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<YAnnotRegex>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_constructor_requiring_nonconst_then_requiring_const_ok(self):
        source = '''
            struct X {};
            
            struct Y {
              Y(X&) {}
            };
            
            struct Z {
              Z(const X&) {}
            };
    
            Poco::Fruit::Component<Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<Y(X&)>()
                .registerConstructor<Z(const X&)>()
                .registerConstructor<X()>();
            }
            
            int main() {
              Poco::Fruit::Injector<Y, Z> injector(getRootComponent);
              injector.get<Y>();
              injector.get<Z>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_constructor_requiring_nonconst_then_requiring_const_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            
            struct Y {
              Y(X&) {}
            };
            
            struct Z {
              Z(const X&) {}
            };
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<Y(X&)>()
                .registerConstructor<Z(const X&)>();
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_constructor_requiring_const_then_requiring_nonconst_ok(self):
        source = '''
            struct X {};
            
            struct Y {
              Y(const X&) {}
            };
            
            struct Z {
              Z(X&) {}
            };
    
            Poco::Fruit::Component<Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<Y(const X&)>()
                .registerConstructor<Z(X&)>()
                .registerConstructor<X()>();
            }
            
            int main() {
              Poco::Fruit::Injector<Y, Z> injector(getRootComponent);
              injector.get<Y>();
              injector.get<Z>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_constructor_requiring_const_then_requiring_nonconst_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            
            struct Y {
              Y(const X&) {}
            };
            
            struct Z {
              Z(X&) {}
            };
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<Y(const X&)>()
                .registerConstructor<Z(X&)>();
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Y**', r'Y\*\*'),
        ('std::shared_ptr<Y>*', r'std::shared_ptr<Y>\*'),
        ('std::nullptr_t', r'(std::)?nullptr(_t)?'),
        ('Y*&', r'Y\*&'),
        ('Y(*)()', r'Y(\((__cdecl)?\*\))?\((void)?\)'),
        ('Poco::Fruit::Annotated<Annotation1, Y**>', r'Y\*\*'),
    ])
    def test_register_constructor_with_param_error_type_not_injectable(self, YVariant, YVariantRegex):
        source = '''
            struct Y {};
            struct X {
              X(YVariant);
            };
            
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<X(YVariant)>();
            }
            '''
        expect_compile_error(
            'NonInjectableTypeError<YVariantRegex>',
            'The type T is not injectable.',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_constructor_error_assisted_param(self):
        source = '''
            struct X {
              INJECT(X(ASSISTED(double) factor)) {
                (void) factor;
              }
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<X(Poco::Fruit::Assisted<double>)>();
            }
            '''
        expect_compile_error(
            'AssistedParamInRegisterConstructorSignatureError<X\\(Poco::Fruit::Assisted<double>\\)>',
            'CandidateSignature was used as signature for a registerConstructor.* but it contains an assisted parameter.',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_implicit_register_constructor_error_assisted_param(self):
        source = '''
            struct X {
              INJECT(X(ASSISTED(double) factor)) {
                (void) factor;
              }
            };
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'AssistedParamInRegisterConstructorSignatureError<X\\(Poco::Fruit::Assisted<double>\\)>',
            'CandidateSignature was used as signature for a registerConstructor.* but it contains an assisted parameter.',
            COMMON_DEFINITIONS,
            source,
            locals())



if __name__ == '__main__':
    absltest.main()
