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

class TestInstallComponentFunctions(parameterized.TestCase):
    def test_install_component_functions_deduped_against_previous_install_no_args(self):
        source = '''
            int num_executions = 0;
            
            Poco::Fruit::Component<int> getChildComponent() {
              static int n = 5;
              ++num_executions;
              return Poco::Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Poco::Fruit::Component<> getMiddleComponent() {
              return Poco::Fruit::createComponent()
                  .install(getChildComponent);
            }
            
            Poco::Fruit::Component<int> getMainComponent() {
              return Poco::Fruit::createComponent()
                  .install(getMiddleComponent)
                  .installComponentFunctions(Poco::Fruit::componentFunction(getChildComponent));
            }
    
            int main() {
              Poco::Fruit::Injector<int> injector(getMainComponent);
              int n = injector.get<int>();
              Assert(n == 5);
              Assert(num_executions == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_deduped_against_following_install_no_args(self):
        source = '''
            int num_executions = 0;
            
            Poco::Fruit::Component<int> getChildComponent() {
              static int n = 5;
              ++num_executions;
              return Poco::Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Poco::Fruit::Component<> getMiddleComponent() {
              return Poco::Fruit::createComponent()
                  .installComponentFunctions(Poco::Fruit::componentFunction(getChildComponent));
            }
            
            Poco::Fruit::Component<int> getMainComponent() {
              return Poco::Fruit::createComponent()
                  .install(getMiddleComponent)
                  .install(getChildComponent);
            }
    
            int main() {
              Poco::Fruit::Injector<int> injector(getMainComponent);
              int n = injector.get<int>();
              Assert(n == 5);
              Assert(num_executions == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_deduped_against_previous_install_with_args(self):
        source = '''
            int num_executions = 0;
            
            Poco::Fruit::Component<int> getChildComponent(int) {
              static int n = 5;
              ++num_executions;
              return Poco::Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Poco::Fruit::Component<> getMiddleComponent() {
              return Poco::Fruit::createComponent()
                  .install(getChildComponent, 42);
            }
                    
            Poco::Fruit::Component<int> getMainComponent() {
              return Poco::Fruit::createComponent()
                  .install(getMiddleComponent)
                  .installComponentFunctions(Poco::Fruit::componentFunction(getChildComponent, 42));
            }
    
            int main() {
              Poco::Fruit::Injector<int> injector(getMainComponent);
              int n = injector.get<int>();
              Assert(n == 5);
              Assert(num_executions == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_deduped_against_following_install_with_args(self):
        source = '''
            int num_executions = 0;
            
            Poco::Fruit::Component<int> getChildComponent(int) {
              static int n = 5;
              ++num_executions;
              return Poco::Fruit::createComponent()
                  .bindInstance(n);
            }
            
            Poco::Fruit::Component<> getMiddleComponent() {
              return Poco::Fruit::createComponent()
                  .installComponentFunctions(Poco::Fruit::componentFunction(getChildComponent, 42));
            }
                            
            Poco::Fruit::Component<int> getMainComponent() {
              return Poco::Fruit::createComponent()
                  .install(getMiddleComponent)
                  .install(getChildComponent, 42);
            }
    
            int main() {
              Poco::Fruit::Injector<int> injector(getMainComponent);
              int n = injector.get<int>();
              Assert(n == 5);
              Assert(num_executions == 1);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_same_as_with_previous_install_with_different_args(self):
        source = '''
            int num_executions = 0;
            
            Poco::Fruit::Component<int> getChildComponent(int) {
              static int n = 5;
              ++num_executions;
              return Poco::Fruit::createComponent()
                  .bindInstance(n);
            }
    
            Poco::Fruit::Component<> getMiddleComponent() {
              return Poco::Fruit::createComponent()
                  .install(getChildComponent, 42);
            }
            
            Poco::Fruit::Component<int> getMainComponent() {
              return Poco::Fruit::createComponent()
                  .install(getMiddleComponent)
                  .installComponentFunctions(Poco::Fruit::componentFunction(getChildComponent, 2));
            }
    
            int main() {
              Poco::Fruit::Injector<int> injector(getMainComponent);
              int n = injector.get<int>();
              Assert(n == 5);
              Assert(num_executions == 2);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_same_as_following_install_with_different_args(self):
        source = '''
            int num_executions = 0;
            
            Poco::Fruit::Component<int> getChildComponent(int) {
              static int n = 5;
              ++num_executions;
              return Poco::Fruit::createComponent()
                  .bindInstance(n);
            }
    
            Poco::Fruit::Component<> getMiddleComponent() {
              return Poco::Fruit::createComponent()
                  .installComponentFunctions(Poco::Fruit::componentFunction(getChildComponent, 42));
            }
                    
            Poco::Fruit::Component<int> getMainComponent() {
              return Poco::Fruit::createComponent()
                  .install(getMiddleComponent)
                  .install(getChildComponent, 2);
            }
    
            int main() {
              Poco::Fruit::Injector<int> injector(getMainComponent);
              (void)injector;
              Assert(num_executions == 2);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_install_component_functions_no_component_functions(self):
        source = '''
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent()
                .installComponentFunctions();
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getComponent);
              (void)injector;
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_install_component_functions_one_component_function(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            Poco::Fruit::Component<X> getParentComponent(std::string) {
              return Poco::Fruit::createComponent()
                .registerProvider([]() { return X(5); });
            }
    
            Poco::Fruit::Component<X> getComponent() {
              return Poco::Fruit::createComponent()
                .installComponentFunctions(Poco::Fruit::componentFunction(getParentComponent, std::string("Hello")));
            }
    
            int main() {
              Poco::Fruit::Injector<X> injector(getComponent);
              X x = injector.get<X>();
              Assert(x.n == 5);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_install_component_functions_two_component_functions(self):
        source = '''
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Y {
              int n;
              Y(int n) : n(n) {}
            };
            
            Poco::Fruit::Component<X> getParentComponent1(std::string) {
              return Poco::Fruit::createComponent()
                .registerProvider([]() { return X(5); });
            }
    
            Poco::Fruit::Component<Y> getParentComponent2(std::string) {
              return Poco::Fruit::createComponent()
                  .registerProvider([]() { return Y(42); });
            }
    
            Poco::Fruit::Component<X, Y> getComponent() {
              return Poco::Fruit::createComponent()
                  .installComponentFunctions(
                      Poco::Fruit::componentFunction(getParentComponent1, std::string("Hello")),
                      Poco::Fruit::componentFunction(getParentComponent2, std::string("World")));
            }
    
            int main() {
              Poco::Fruit::Injector<X, Y> injector(getComponent);
              X x = injector.get<X>();
              Y y = injector.get<Y>();
              Assert(x.n == 5);
              Assert(y.n == 42);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_install_component_functions_with_template_parameter_pack_unpacking(self):
        source = '''
            template <typename T>
            struct GetComponentHolder;
        
            struct X {
              int n;
              X(int n) : n(n) {}
            };
            
            struct Y {
              int n;
              Y(int n) : n(n) {}
            };
            
            template <>
            struct GetComponentHolder<X> {
                static Poco::Fruit::Component<X> getComponent(std::string) {
                  return Poco::Fruit::createComponent()
                    .registerProvider([]() { return X(5); });
                }
            };
    
            template <>
            struct GetComponentHolder<Y> {
                static Poco::Fruit::Component<Y> getComponent(std::string) {
                  return Poco::Fruit::createComponent()
                      .registerProvider([]() { return Y(42); });
                } 
            };
    
            template <typename... Ts>
            Poco::Fruit::Component<Ts...> getComponent() {
              return Poco::Fruit::createComponent()
                  .installComponentFunctions(
                      Poco::Fruit::componentFunction(GetComponentHolder<Ts>::getComponent, std::string("Hello"))...);
            }
    
            int main() {
              Poco::Fruit::Injector<X, Y> injector(getComponent<X, Y>);
              X x = injector.get<X>();
              Y y = injector.get<Y>();
              Assert(x.n == 5);
              Assert(y.n == 42);
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_install_component_functions_wrong_argument_type(self):
        source = '''
            Poco::Fruit::Component<> getMainComponent() {
              return Poco::Fruit::createComponent()
                  .installComponentFunctions(42);
            }
            '''
        expect_compile_error(
            'IncorrectArgTypePassedToInstallComponentFuntionsError<int>',
            'All arguments passed to installComponentFunctions.. must be Poco::Fruit::ComponentFunction<...> objects but an '
            'argument with type Arg was passed instead.',
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
