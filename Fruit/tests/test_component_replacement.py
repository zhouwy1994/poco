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

    '''

class TestComponentReplacement(parameterized.TestCase):
    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_success(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              int n = injector.get<int>();
              Assert(n == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_success_across_normalized_component(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<> getRootComponent1() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation);
            }
            
            Fruit::Component<int> getRootComponent2() {
              return Fruit::createComponent()
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::NormalizedComponent<> normalizedComponent(getRootComponent1);
              Fruit::Injector<int> injector(normalizedComponent, getRootComponent2);
              int n = injector.get<int>();
              Assert(n == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_installed_using_component_function_success(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .installComponentFunctions(Fruit::componentFunction(ReplacedComponentInstallation));
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              int n = injector.get<int>();
              Assert(n == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_replace_component_success_with_conversion(self):
        source = '''
            Fruit::Component<int> getReplacedComponent(std::string) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(double, std::string, int) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .replace(getReplacedComponent, "Hi").with(getReplacementComponent, 2.0, "Hello", 12)
                  .install(getReplacedComponent, "Hi");
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              int n = injector.get<int>();
              Assert(n == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_replace_component_installed_using_component_function_success_with_conversion(self):
        source = '''
            Fruit::Component<int> getReplacedComponent(std::string) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(double, std::string, int) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .replace(getReplacedComponent, "Hi").with(getReplacementComponent, 2.0, "Hello", 12)
                  .installComponentFunctions(Fruit::componentFunction(getReplacedComponent, "Hi"));
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              int n = injector.get<int>();
              Assert(n == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent', 'getReplacementComponent', 'getReplacementReplacementComponent'),
        ('double', 'getReplacedComponent, 1.0', 'getReplacementComponent, 1.0', 'getReplacementReplacementComponent, 1.0'),
    ])
    def test_replace_component_chain_success(self,
            ComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentInstallation, ReplacementReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementReplacementComponent(ComponentParamTypes) {
              static int n = 30;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .replace(ReplacementComponentInstallation).with(ReplacementReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              int n = injector.get<int>();
              Assert(n == 30);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent', 'getReplacementComponent', 'getReplacementReplacementComponent'),
        ('double', 'getReplacedComponent, 1.0', 'getReplacementComponent, 1.0', 'getReplacementReplacementComponent, 1.0'),
    ])
    def test_replace_component_chain_other_order_success(self,
            ComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentInstallation, ReplacementReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementReplacementComponent(ComponentParamTypes) {
              static int n = 30;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacementComponentInstallation).with(ReplacementReplacementComponentInstallation)
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              int n = injector.get<int>();
              Assert(n == 30);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_replace_component_different_type_error(self):
        source = '''
            Fruit::Component<int> getReplacedComponent();
            Fruit::Component<double> getReplacementComponent();
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(getReplacedComponent).with(getReplacementComponent);
            }
            '''
        expect_generic_compile_error(
            # Clang
            r'candidate template ignored: could not match .Component<int>. against .Component<double>.'
            # GCC
            r'|mismatched types .int. and .double.'
            # MSVC
            r'|could not deduce template argument for .Fruit::Component<int> \(__cdecl \*\)\(FormalArgs...\). from .Fruit::Component<double> \(void\).',
            COMMON_DEFINITIONS,
            source)

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_already_replaced_consistent_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              int n = injector.get<int>();
              Assert(n == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_already_replaced_across_normalized_component_consistent_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<> getRootComponent1() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation);
            }
            
            Fruit::Component<int> getRootComponent2() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::NormalizedComponent<> normalizedComponent(getRootComponent1);
              Fruit::Injector<int> injector(normalizedComponent, getRootComponent2);
              int n = injector.get<int>();
              Assert(n == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent', 'getOtherReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")', 'getOtherReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_already_replaced_inconsistent_error(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation, OtherReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getOtherReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 30;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .replace(ReplacedComponentInstallation).with(OtherReplacementComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              (void) injector;
            }
            '''
        expect_runtime_error(
            r'Fatal injection error: the component function at (0x)?[0-9a-fA-F]* with signature '
            r'(class )?Fruit::Component<int> \((__cdecl)?\*\)\((void)?ReplacedComponentParamTypes\) was replaced '
            r'\(using .replace\(...\).with\(...\)\) with both the component function at (0x)?[0-9a-fA-F]* with signature '
            r'(class )?Fruit::Component<int> \((__cdecl)?\*\)\(.*\) and the component function at '
            r'(0x)?[0-9a-fA-F]* with signature (class )?Fruit::Component<int> \((__cdecl)?\*\)\(.*\) .',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent', 'getOtherReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")', 'getOtherReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_already_replaced_across_normalized_component_inconsistent_error(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation, OtherReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getOtherReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 30;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<> getRootComponent1() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation);
            }
            
            Fruit::Component<> getRootComponent2() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(OtherReplacementComponentInstallation);
            }
            
            int main() {
              Fruit::NormalizedComponent<> normalizedComponent(getRootComponent1);
              Fruit::Injector<> injector(normalizedComponent, getRootComponent2);
              (void) injector;
            }
            '''
        expect_runtime_error(
            r'Fatal injection error: the component function at (0x)?[0-9a-fA-F]* with signature '
            r'(class )?Fruit::Component<int> \((__cdecl)?\*\)\((void)?ReplacedComponentParamTypes\) was replaced '
            r'\(using .replace\(...\).with\(...\)\) with both the component function at (0x)?[0-9a-fA-F]* with signature '
            r'(class )?Fruit::Component<int> \((__cdecl)?\*\)\(.*\) and the component function at '
            r'(0x)?[0-9a-fA-F]* with signature (class )?Fruit::Component<int> \((__cdecl)?\*\)\(.*\) .',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_after_install_error(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent() {
              return Fruit::createComponent()
                  .install(ReplacedComponentInstallation)
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<int> injector(getRootComponent);
              (void) injector;
            }
            '''
        expect_runtime_error(
            r'Fatal injection error: unable to replace \(using .replace\(...\).with\(...\)\) the component function at '
            r'(0x)?[0-9a-fA-F]* with signature (class )?Fruit::Component<int> \((__cdecl)?\*\)\((void)?ReplacedComponentParamTypes\) with the '
            r'component function at (0x)?[0-9a-fA-F]* with signature '
            r'(class )?Fruit::Component<int> \((__cdecl)?\*\)\(.*\) because the former component function '
            r'was installed before the .replace\(...\).with\(...\).',
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_after_install_across_normalized_component_error(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<int> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Fruit::Component<int> getRootComponent1() {
              return Fruit::createComponent()
                  .install(ReplacedComponentInstallation);
            }
            
            Fruit::Component<> getRootComponent2() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation);
            }
            
            int main() {
              Fruit::NormalizedComponent<int> normalizedComponent(getRootComponent1);
              Fruit::Injector<int> injector(normalizedComponent, getRootComponent2);
              (void) injector;
            }
            '''
        expect_runtime_error(
            r'Fatal injection error: unable to replace \(using .replace\(...\).with\(...\)\) the component function at '
            r'(0x)?[0-9a-fA-F]* with signature (class )?Fruit::Component<int> \((__cdecl)?\*\)\((void)?ReplacedComponentParamTypes\) with the '
            r'component function at (0x)?[0-9a-fA-F]* with signature '
            r'(class )?Fruit::Component<int> \((__cdecl)?\*\)\(.*\) because the former component function '
            r'was installed before the .replace\(...\).with\(...\).',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('', 'getReplacedComponent', '', 'getReplacementComponent'),
        ('double', 'getReplacedComponent, 1.0', 'std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_unused_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 0);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_used_multiple_times_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 1);
              Assert(*(multibindings[0]) == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_also_installed_directly_before_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .install(ReplacementComponentInstallation)
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 1);
              Assert(*(multibindings[0]) == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_also_installed_directly_after_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation)
                  .install(ReplacementComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 1);
              Assert(*(multibindings[0]) == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_also_installed_directly_before_across_normalized_component_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent1() {
              return Fruit::createComponent()
                  .install(ReplacementComponentInstallation);
            }
            
            Fruit::Component<> getRootComponent2() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::NormalizedComponent<> normalizedComponent(getRootComponent1);
              Fruit::Injector<> injector(normalizedComponent, getRootComponent2);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 1);
              Assert(*(multibindings[0]) == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent'),
        ('double', 'getReplacedComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_component_also_installed_directly_after_across_normalized_component_ok(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent1() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation);
            }
            
            Fruit::Component<> getRootComponent2() {
              return Fruit::createComponent()
                  .install(ReplacementComponentInstallation);
            }
            
            int main() {
              Fruit::NormalizedComponent<> normalizedComponent(getRootComponent1);
              Fruit::Injector<> injector(normalizedComponent, getRootComponent2);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 1);
              Assert(*(multibindings[0]) == 20);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('', 'getReplacedComponent', 'getOtherReplacementComponent'),
        ('double', 'getReplacedComponent, 1.0', 'getOtherReplacementComponent, 1.0'),
    ], [
        ('', 'getReplacementComponent'),
        ('std::string', 'getReplacementComponent, std::string("Hello, world")'),
    ])
    def test_replace_multiple_components_with_same(self,
            ReplacedComponentParamTypes, ReplacedComponentInstallation, OtherReplacedComponentInstallation, ReplacementComponentParamTypes, ReplacementComponentInstallation):
        source = '''
            Fruit::Component<> getReplacedComponent(ReplacedComponentParamTypes) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getOtherReplacementComponent(ReplacedComponentParamTypes) {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent(ReplacementComponentParamTypes) {
              static int n = 30;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(ReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .replace(OtherReplacedComponentInstallation).with(ReplacementComponentInstallation)
                  .install(ReplacedComponentInstallation)
                  .install(OtherReplacedComponentInstallation);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 1);
              Assert(*(multibindings[0]) == 30);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_replace_component_one_set_of_args_only(self):
        source = '''
            Fruit::Component<> getReplacedComponent(double) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent() {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(getReplacedComponent, 1.0).with(getReplacementComponent)
                  .install(getReplacedComponent, 1.0)
                  .install(getReplacedComponent, 5.0);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 2);
              Assert(*(multibindings[0]) == 20);
              Assert(*(multibindings[1]) == 10);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_replace_component_already_replaced_with_different_args(self):
        source = '''
            Fruit::Component<> getReplacedComponent(double) {
              static int n = 10;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getReplacementComponent() {
              static int n = 20;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getOtherReplacementComponent() {
              static int n = 30;
              return Fruit::createComponent()
                  .addInstanceMultibinding(n);
            }
            
            Fruit::Component<> getRootComponent() {
              return Fruit::createComponent()
                  .replace(getReplacedComponent, 1.0).with(getReplacementComponent)
                  .replace(getReplacedComponent, 5.0).with(getOtherReplacementComponent)
                  .install(getReplacedComponent, 1.0)
                  .install(getReplacedComponent, 5.0);
            }
            
            int main() {
              Fruit::Injector<> injector(getRootComponent);
              
              std::vector<int*> multibindings = injector.getMultibindings<int>();
              Assert(multibindings.size() == 2);
              Assert(*(multibindings[0]) == 20);
              Assert(*(multibindings[1]) == 30);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
