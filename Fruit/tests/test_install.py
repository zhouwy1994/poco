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
    '''

class TestInstall(parameterized.TestCase):
    @parameterized.parameters([
        ('X', 'X'),
        ('X', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, X>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_success(self, XParamInChildComponent, XParamInRootComponent):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
    
            Poco::Fruit::Component<XParamInChildComponent> getChildComponent() {
              return Poco::Fruit::createComponent()
                .registerProvider<XParamInChildComponent()>([]() { return X(5); });
            }
    
            Poco::Fruit::Component<XParamInRootComponent> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent);
            }
    
            int main() {
              Poco::Fruit::Injector<XParamInRootComponent> injector(getRootComponent);
              X x = injector.get<XParamInRootComponent>();
              Assert(x.n == 5);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', 'X'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, X>'),
    ])
    def test_install_error_child_component_provides_const(self, XParamInChildComponent, XParamInRootComponent):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<XParamInChildComponent> getChildComponent();
    
            Poco::Fruit::Component<XParamInRootComponent> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent);
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<XParamInRootComponent>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X'),
        ('X', 'const X'),
        ('const X', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, X>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_with_requirements_success(self, ProvidedXParam, RequiredXParam):
        ProvidedXParamWithoutConst = ProvidedXParam.replace('const ', '')
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
    
            struct Y {
              X x;
              Y(X x): x(x) {}
            };
    
            Poco::Fruit::Component<Poco::Fruit::Required<RequiredXParam>, Y> getChildComponent1() {
              return Poco::Fruit::createComponent()
                .registerProvider<Y(RequiredXParam)>([](X x) { return Y(x); });
            }
    
            Poco::Fruit::Component<ProvidedXParam> getChildComponent2() {
              return Poco::Fruit::createComponent()
                .registerProvider<ProvidedXParamWithoutConst()>([]() { return X(5); });
            }
    
            Poco::Fruit::Component<Y> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent1)
                .install(getChildComponent2);
            }
    
            int main() {
              Poco::Fruit::Injector<Y> injector(getRootComponent);
              Y y = injector.get<Y>();
              Assert(y.x.n == 5);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', 'X'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, X>'),
    ])
    def test_with_requirements_error_only_nonconst_provided(self, ProvidedXParam, RequiredXParam):
        source = '''
            struct X {};
            struct Y {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<RequiredXParam>, Y> getChildComponent1();
    
            Poco::Fruit::Component<ProvidedXParam> getChildComponent2();
    
            Poco::Fruit::Component<Y> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent1)
                .install(getChildComponent2);
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<RequiredXParam>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('const X', 'X'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', 'Poco::Fruit::Annotated<Annotation1, X>'),
    ])
    def test_with_requirements_error_only_nonconst_provided_reversed_install_order(self, ProvidedXParam, RequiredXParam):
        source = '''
            struct X {};
            struct Y {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<RequiredXParam>, Y> getChildComponent1();
    
            Poco::Fruit::Component<ProvidedXParam> getChildComponent2();
    
            Poco::Fruit::Component<Y> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent2)
                .install(getChildComponent1);
            }
            '''
        expect_compile_error(
            'NonConstBindingRequiredButConstBindingProvidedError<RequiredXParam>',
            'The type T was provided as constant, however one of the constructors/providers/factories in this component',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_with_requirements_not_specified_in_child_component_error(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
    
            struct Y {
              X x;
              Y(X x): x(x) {}
            };
    
            Poco::Fruit::Component<Poco::Fruit::Required<X>, Y> getParentYComponent() {
              return Poco::Fruit::createComponent()
                .registerProvider([](X x) { return Y(x); });
            }
    
            // We intentionally don't have Poco::Fruit::Required<X> here, we want to test that this results in an error.
            Poco::Fruit::Component<Y> getYComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentYComponent);
            }
            '''
        expect_compile_error(
            'NoBindingFoundError<X>',
            'No explicit binding nor C::Inject definition was found for T',
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('X', 'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, const X>'),
    ])
    def test_install_requiring_nonconst_then_install_requiring_const_ok(self, XAnnot, ConstXAnnot):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<XAnnot>, Y> getChildComponent1() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<Y()>();
            }
            
            Poco::Fruit::Component<Poco::Fruit::Required<ConstXAnnot>, Z> getChildComponent2() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<Z()>();
            }
    
            Poco::Fruit::Component<Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent1)
                .install(getChildComponent2)
                .registerConstructor<XAnnot()>();
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

    def test_install_requiring_nonconst_then_install_requiring_const_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<X>, Y> getChildComponent1();
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, Z> getChildComponent2();
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent1)
                .install(getChildComponent2);
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_requiring_const_then_install_requiring_nonconst_ok(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, Y> getChildComponent1() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<Y()>();
            }
            
            Poco::Fruit::Component<Poco::Fruit::Required<X>, Z> getChildComponent2() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<Z()>();
            }
    
            Poco::Fruit::Component<Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent1)
                .install(getChildComponent2)
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

    def test_install_requiring_const_then_install_requiring_nonconst_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, Y> getChildComponent1();
            Poco::Fruit::Component<Poco::Fruit::Required<X>, Z> getChildComponent2();
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, Y, Z> getRootComponent() {
              return Poco::Fruit::createComponent()
                .install(getChildComponent1)
                .install(getChildComponent2);
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_with_args_success(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Arg {
              Arg(int) {}
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&) {
              return true;
            }
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&) {
                  return 0;
                }
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg, Arg) {
              return Poco::Fruit::createComponent()
                .registerProvider([]() { return X(5); });
            }
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), Arg{}, 15);
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getComponent);
              X x = injector.get<X>();
              Assert(x.n == 5);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_install_with_args_error_not_move_constructible(self):
        source = '''
            struct Arg {
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = delete;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), Arg{});
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg::Arg\(Arg&&\).'
            r'|error: call to deleted constructor of .Arg.'
            r'|.Arg::Arg\(const Arg &\).: cannot convert argument 1 from .std::_Tuple_val<Arg>. to .const Arg &.'
            r'|.Arg::Arg\(Arg &&\).: cannot convert argument 1 from .std::_Tuple_val<Arg>. to .const Arg &.',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_move_constructible_with_conversion(self):
        source = '''
            struct Arg {
              Arg(int) {}
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = delete;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), 15);
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg::Arg\(Arg&&\).'
            r'|error: call to deleted constructor of .Arg.'
            r'|.Arg::Arg\((int|Arg &&)\).: cannot convert argument 1 from .std::_Tuple_val<Arg>. to .int.',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_copy_constructible(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Arg {
              Arg() = default;
              Arg(const Arg&) = delete;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), Arg{});
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg::Arg\(const Arg&\).'
            r'|error: call to deleted constructor of .Arg.'
            r'|error C2280: .Arg::Arg\(const Arg &\).: attempting to reference a deleted function',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_copy_constructible_with_conversion(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Arg {
              Arg(int) {}
              Arg() = default;
              Arg(const Arg&) = delete;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), 15);
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg::Arg\(const Arg&\).'
            r'|error: call to deleted constructor of .Arg.'
            r'|error C2280: .Arg::Arg\(const Arg &\).: attempting to reference a deleted function',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_move_assignable(self):
        source = '''
            struct Arg {
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = delete;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), Arg{});
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg& Arg::operator=\(Arg&&\).'
            r'|error: overload resolution selected deleted operator .=.'
            r'|error C2280: .Arg &Arg::operator =\(Arg &&\).: attempting to reference a deleted function',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_move_assignable_with_conversion(self):
        source = '''
            struct Arg {
              Arg(int) {}
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = delete;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), 15);
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg& Arg::operator=\(Arg&&\).'
            r'|error: overload resolution selected deleted operator .=.'
            r'|error C2280: .Arg &Arg::operator =\(Arg &&\).: attempting to reference a deleted function',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_copy_assignable(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Arg {
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = delete;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), Arg{});
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg& Arg::operator=\(const Arg&\).'
            r'|error: overload resolution selected deleted operator .=.'
            r'|error C2280: .Arg &Arg::operator =\(const Arg &\).: attempting to reference a deleted function',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_copy_assignable_with_conversion(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Arg {
              Arg(int) {}
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = delete;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), 15);
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .Arg& Arg::operator=\(const Arg&\).'
            r'|error: overload resolution selected deleted operator .=.'
            r'|error C2280: .Arg &Arg::operator =\(const Arg &\).: attempting to reference a deleted function',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_equality_comparable(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Arg {
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), Arg{});
            }
            '''
        expect_generic_compile_error(
            r'error: no match for .operator==. \(operand types are .const Arg. and .const Arg.\)'
            r'|error: invalid operands to binary expression \(.const Arg. and .const Arg.\)'
            r'|error C2676: binary .==.: .const Arg. does not define this operator',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_equality_comparable_with_conversion(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Arg {
              Arg(int) {}
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            namespace std {
              template <>
              struct hash<Arg> {
                size_t operator()(const Arg&);
              };
            }
    
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), 15);
            }
            '''
        expect_generic_compile_error(
            r'error: no match for .operator==. \(operand types are .const Arg. and .const Arg.\)'
            r'|error: invalid operands to binary expression \(.const Arg. and .const Arg.\)'
            r'|error C2676: binary .==.: .const Arg. does not define this operator',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_hashable(self):
        source = '''
            struct Arg {
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), Arg{});
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .std::hash<Arg>::hash\(\).'
            r'|error: call to implicitly-deleted default constructor of .std::hash<Arg>.'
            r'|error: invalid use of incomplete type .struct std::hash<Arg>.'
            r'|error: implicit instantiation of undefined template .std::(__1::)?hash<Arg>.'
            r'|error C2338: The C\+\+ Standard doesn.t provide a hash for this type.'
            r'|error C2064: term does not evaluate to a function taking 1 arguments',
            COMMON_DEFINITIONS,
            source)

    def test_install_with_args_error_not_hashable_with_conversion(self):
        source = '''
            struct Arg {
              Arg(int) {}
              Arg() = default;
              Arg(const Arg&) = default;
              Arg(Arg&&) = default;
              Arg& operator=(const Arg&) = default;
              Arg& operator=(Arg&&) = default;
            };
            
            bool operator==(const Arg&, const Arg&);
            
            Poco::Fruit::Component<X> getParentComponent(int, std::string, Arg);
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getParentComponent, 5, std::string("Hello"), 15);
            }
            '''
        expect_generic_compile_error(
            r'error: use of deleted function .std::hash<Arg>::hash\(\).'
            r'|error: call to implicitly-deleted default constructor of .std::hash<Arg>.'
            r'|error: invalid use of incomplete type .struct std::hash<Arg>.'
            r'|error: implicit instantiation of undefined template .std::(__1::)?hash<Arg>.'
            r'|error C2338: The C\+\+ Standard doesn.t provide a hash for this type.'
            r'|error C2064: term does not evaluate to a function taking 1 arguments',
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_install_component_functions_deduped(self, XAnnot):
        source = '''
            struct X {};
    
            X x;
    
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding<XAnnot, X>(x);
            }
    
            Poco::Fruit::Component<> getComponent2() {
              return Poco::Fruit::createComponent()
                .install(getComponent);
            }
    
            Poco::Fruit::Component<> getComponent3() {
              return Poco::Fruit::createComponent()
                .install(getComponent);
            }
    
            Poco::Fruit::Component<> getComponent4() {
              return Poco::Fruit::createComponent()
                .install(getComponent2)
                .install(getComponent3);
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getComponent4);
    
              // We test multibindings because the effect on other bindings is not user-visible (that only affects
              // performance).
              std::vector<X*> multibindings = injector.getMultibindings<XAnnot>();
              Assert(multibindings.size() == 1);
              Assert(multibindings[0] == &x);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_install_component_functions_deduped_across_normalized_component(self, XAnnot):
        source = '''
            struct X {};
    
            X x;
    
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding<XAnnot, X>(x);
            }
    
            Poco::Fruit::Component<> getComponent2() {
              return Poco::Fruit::createComponent()
                .install(getComponent);
            }
    
            Poco::Fruit::Component<> getComponent3() {
              return Poco::Fruit::createComponent()
                .install(getComponent);
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<> normalizedComponent(getComponent2);
              Poco::Fruit::Injector<> injector(normalizedComponent, getComponent3);
    
              // We test multibindings because the effect on other bindings is not user-visible (that only affects
              // performance).
              std::vector<X*> multibindings = injector.getMultibindings<XAnnot>();
              Assert(multibindings.size() == 1);
              Assert(multibindings[0] == &x);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_install_component_functions_with_args_deduped(self, XAnnot):
        source = '''
            struct X {};
    
            X x;
    
            Poco::Fruit::Component<> getComponent(int) {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding<XAnnot, X>(x);
            }
    
            Poco::Fruit::Component<> getComponent2() {
              return Poco::Fruit::createComponent()
                .install(getComponent, 1);
            }
    
            Poco::Fruit::Component<> getComponent3() {
              return Poco::Fruit::createComponent()
                .install(getComponent, 1);
            }
    
            Poco::Fruit::Component<> getComponent4() {
              return Poco::Fruit::createComponent()
                .install(getComponent2)
                .install(getComponent3);
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getComponent4);
    
              // We test multibindings because the effect on other bindings is not user-visible (that only affects
              // performance).
              std::vector<X*> multibindings = injector.getMultibindings<XAnnot>();
              Assert(multibindings.size() == 1);
              Assert(multibindings[0] == &x);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'X',
        'Poco::Fruit::Annotated<Annotation1, X>',
    ])
    def test_install_component_functions_different_args_not_deduped(self, XAnnot):
        source = '''
            struct X {};
    
            X x;
    
            Poco::Fruit::Component<> getComponent(int) {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding<XAnnot, X>(x);
            }
    
            Poco::Fruit::Component<> getComponent2() {
              return Poco::Fruit::createComponent()
                .install(getComponent, 1);
            }
    
            Poco::Fruit::Component<> getComponent3() {
              return Poco::Fruit::createComponent()
                .install(getComponent, 2);
            }
    
            Poco::Fruit::Component<> getComponent4() {
              return Poco::Fruit::createComponent()
                .install(getComponent2)
                .install(getComponent3);
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getComponent4);
    
              // We test multibindings because the effect on other bindings is not user-visible (it only affects
              // performance).
              std::vector<X*> multibindings = injector.getMultibindings<XAnnot>();
              Assert(multibindings.size() == 2);
              Assert(multibindings[0] == &x);
              Assert(multibindings[1] == &x);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_loop(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
            
            // X -> Y -> Z -> Y
            
            Poco::Fruit::Component<X> getXComponent();
            Poco::Fruit::Component<Y> getYComponent();
            Poco::Fruit::Component<Z> getZComponent();
    
            Poco::Fruit::Component<X> getXComponent() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<X()>()
                  .install(getYComponent);
            }
    
            Poco::Fruit::Component<Y> getYComponent() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<Y()>()
                  .install(getZComponent);
            }
    
            Poco::Fruit::Component<Z> getZComponent() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<Z()>()
                  .install(getYComponent);
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getXComponent);
              (void)injector;
            }
            '''
        expect_runtime_error(
            r'Component installation trace \(from top-level to the most deeply-nested\):\n'
            r'(class )?Poco::Fruit::Component<(struct )?X> ?\((__cdecl)?\*\)\((void)?\)\n'
            r'<-- The loop starts here\n'
            r'(class )?Poco::Fruit::Component<(struct )?Y> ?\((__cdecl)?\*\)\((void)?\)\n'
            r'(class )?Poco::Fruit::Component<(struct )?Z> ?\((__cdecl)?\*\)\((void)?\)\n'
            r'(class )?Poco::Fruit::Component<(struct )?Y> ?\((__cdecl)?\*\)\((void)?\)\n',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_different_arguments_loop_not_reported(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
            
            // X -> Y(1) -> Z -> Y(2)
            
            Poco::Fruit::Component<X> getXComponent();
            Poco::Fruit::Component<Y> getYComponent(int);
            Poco::Fruit::Component<Z> getZComponent();
    
            Poco::Fruit::Component<X> getXComponent() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<X()>()
                  .install(getYComponent, 1);
            }
    
            Poco::Fruit::Component<Y> getYComponent(int n) {
                if (n == 1) {
                    return Poco::Fruit::createComponent()
                        .registerConstructor<Y()>()
                        .install(getZComponent);
                } else {
                    return Poco::Fruit::createComponent()
                        .registerConstructor<Y()>();
                }
            }
    
            Poco::Fruit::Component<Z> getZComponent() {
              return Poco::Fruit::createComponent()
                  .registerConstructor<Z()>()
                  .install(getYComponent, 2);
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getXComponent);
              injector.get<X>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
