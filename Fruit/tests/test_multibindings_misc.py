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

    struct Listener;

    struct X {};
        
    struct Annotation {};
    struct Annotation1 {};
    using ListenerAnnot = Poco::Fruit::Annotated<Annotation, Listener>;
    '''

class TestMultibindingsMisc(parameterized.TestCase):
    def test_get_none(self):
        source = '''
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getComponent);
    
              std::vector<X*> multibindings = injector.getMultibindings<X>();
              (void) multibindings;
              Assert(multibindings.empty());
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_multiple_various_kinds(self):
        source = '''
            static int numNotificationsToListener1 = 0;
            static int numNotificationsToListener2 = 0;
            static int numNotificationsToListener3 = 0;
    
            struct Listener {
            public:
              virtual ~Listener() = default;
    
              virtual void notify() = 0;
            };
    
            struct Listener1 : public Listener {
            public:
              INJECT(Listener1()) = default;
    
              virtual ~Listener1() = default;
    
              void notify() override {
                ++numNotificationsToListener1;
              }
            };
    
            struct Writer {
            public:
              virtual void write(std::string s) = 0;
            };
    
            struct StdoutWriter : public Writer {
            public:
              INJECT(StdoutWriter()) = default;
    
              void write(std::string s) override {
                std::cout << s << std::endl;
              }
            };
    
            struct Listener2 : public Listener {
            private:
              Writer* writer;
    
            public:
              INJECT(Listener2(Writer* writer))
                : writer(writer) {
              }
    
              virtual ~Listener2() = default;
    
              void notify() override {
                (void) writer;
                ++numNotificationsToListener2;
              }
            };
    
            struct Listener3 : public Listener {
            private:
              Writer* writer;
    
            public:
              INJECT(Listener3(Writer* writer))
                : writer(writer) {
              }
    
              virtual ~Listener3() = default;
    
              void notify() override {
                (void) writer;
                ++numNotificationsToListener3;
              }
            };
    
            Poco::Fruit::Component<> getListenersComponent() {
              return Poco::Fruit::createComponent()
                .bind<Writer, StdoutWriter>()
                // Note: this is just to exercise the other method, but in real code you should split this in
                // an addMultibinding<Listener, Listener1> and a registerProvider with the lambda.
                .addMultibindingProvider([]() {
                  Listener1* listener1 = new Listener1();
                  return static_cast<Listener*>(listener1);
                })
                .addMultibinding<Listener, Listener2>()
                .addMultibinding<ListenerAnnot, Listener3>();
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getListenersComponent);
              std::vector<Listener*> listeners = injector.getMultibindings<Listener>();
              for (Listener* listener : listeners) {
                listener->notify();
              }
    
              std::vector<Listener*> listeners2 = injector.getMultibindings<Listener>();
              Assert(listeners == listeners2);
    
              if (numNotificationsToListener1 != 1 || numNotificationsToListener2 != 1
                || numNotificationsToListener3 != 0) {
                abort();
              }
    
              std::vector<Listener*> listenersWithAnnotation = injector.getMultibindings<ListenerAnnot>();
              for (Listener* listener : listenersWithAnnotation) {
                listener->notify();
              }
    
              if (numNotificationsToListener1 != 1 || numNotificationsToListener2 != 1
                || numNotificationsToListener3 != 1) {
                abort();
              }
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_order(self):
        source = '''
            std::vector<int> numbers = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18};
            // *
            // |-- 0
            // |-- A
            // |   |-- 1
            // |   |-- B
            // |   |   |-- 2
            // |   |   `-- 3
            // |   |-- 4
            // |   |-- C
            // |   |   |-- 5
            // |   |   |-- 6
            // |   |   |-- D
            // |   |   |   |-- 7
            // |   |   |   |-- E
            // |   |   |   |   |-- 8
            // |   |   |   |   `-- 9
            // |   |   |   `-- 10
            // |   |   |-- 11
            // |   |   |-- F
            // |   |   |   |-- 12
            // |   |   |   `-- 13
            // |   |   `-- 14
            // |   |-- 15
            // |   |-- C (won't be expanded)
            // |   `-- 16
            // |-- 17
            // |-- C (won't be expanded)
            // `-- 18
            
            Poco::Fruit::Component<> getRootComponent();
            Poco::Fruit::Component<> getComponentA();
            Poco::Fruit::Component<> getComponentB();
            Poco::Fruit::Component<> getComponentC();
            Poco::Fruit::Component<> getComponentD();
            Poco::Fruit::Component<> getComponentE();
            Poco::Fruit::Component<> getComponentF();
    
            Poco::Fruit::Component<> getRootComponent() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[0])
                .install(getComponentA)
                .addInstanceMultibinding(numbers[17])
                .install(getComponentC)
                .addInstanceMultibinding(numbers[18]);
            }
            
            Poco::Fruit::Component<> getComponentA() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[1])
                .install(getComponentB)
                .addInstanceMultibinding(numbers[4])
                .install(getComponentC)
                .addInstanceMultibinding(numbers[15])
                .install(getComponentC)
                .addInstanceMultibinding(numbers[16]);
            }
    
            Poco::Fruit::Component<> getComponentB() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[2])
                .addInstanceMultibinding(numbers[3]);
            }
    
            Poco::Fruit::Component<> getComponentC() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[5])
                .addInstanceMultibinding(numbers[6])
                .install(getComponentD)
                .addInstanceMultibinding(numbers[11])
                .install(getComponentF)
                .addInstanceMultibinding(numbers[14]);
            }
    
            Poco::Fruit::Component<> getComponentD() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[7])
                .install(getComponentE)
                .addInstanceMultibinding(numbers[10]);
            }
    
            Poco::Fruit::Component<> getComponentE() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[8])
                .addInstanceMultibinding(numbers[9]);
            }
    
            Poco::Fruit::Component<> getComponentF() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[12])
                .addInstanceMultibinding(numbers[13]);
            }
    
            int main() {
              Poco::Fruit::Injector<> injector(getRootComponent);
              std::vector<int*> result_ptrs = injector.getMultibindings<int>();
              std::vector<int> results;
              std::cout << "Results: ";
              for (int* result : result_ptrs) {
                std::cout << *result << ", ";
                results.push_back(*result);
              }
              std::cout << std::endl;
              Assert(results == numbers);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)


    def test_order_with_normalized_component(self):
        source = '''
            std::vector<int> numbers = {
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37};
            // root1
            // |-- 0
            // |-- A
            // |   |-- 1
            // |   |-- B
            // |   |   |-- 2
            // |   |   `-- 3
            // |   |-- 4
            // |   |-- C
            // |   |   |-- 5
            // |   |   |-- 6
            // |   |   |-- D
            // |   |   |   |-- 7
            // |   |   |   |-- E
            // |   |   |   |   |-- 8
            // |   |   |   |   `-- 9
            // |   |   |   `-- 10
            // |   |   |-- 11
            // |   |   |-- F
            // |   |   |   |-- 12
            // |   |   |   `-- 13
            // |   |   `-- 14
            // |   |-- 15
            // |   |-- C (won't be expanded)
            // |   `-- 16
            // |-- 17
            // |-- C (won't be expanded)
            // `-- 18
            
            // root2
            // |-- 19
            // |-- A2
            // |   |-- 20
            // |   |-- B2
            // |   |   |-- 21
            // |   |   `-- 22
            // |   |-- 23
            // |   |-- C2
            // |   |   |-- 24
            // |   |   |-- 25
            // |   |   |-- D2
            // |   |   |   |-- 26
            // |   |   |   |-- E2
            // |   |   |   |   |-- 27
            // |   |   |   |   `-- 28
            // |   |   |   `-- 29
            // |   |   |-- 30
            // |   |   |-- F2
            // |   |   |   |-- 31
            // |   |   |   `-- 32
            // |   |   `-- 33
            // |   |-- 34
            // |   |-- C2 (won't be expanded)
            // |   `-- 35
            // |-- 36
            // |-- C2 (won't be expanded)
            // `-- 37
    
            Poco::Fruit::Component<> getRootComponent();
            Poco::Fruit::Component<> getComponentA();
            Poco::Fruit::Component<> getComponentB();
            Poco::Fruit::Component<> getComponentC();
            Poco::Fruit::Component<> getComponentD();
            Poco::Fruit::Component<> getComponentE();
            Poco::Fruit::Component<> getComponentF();
            
            Poco::Fruit::Component<> getRootComponent2();
            Poco::Fruit::Component<> getComponentA2();
            Poco::Fruit::Component<> getComponentB2();
            Poco::Fruit::Component<> getComponentC2();
            Poco::Fruit::Component<> getComponentD2();
            Poco::Fruit::Component<> getComponentE2();
            Poco::Fruit::Component<> getComponentF2();
    
            Poco::Fruit::Component<> getRootComponent() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[0])
                .install(getComponentA)
                .addInstanceMultibinding(numbers[17])
                .install(getComponentC)
                .addInstanceMultibinding(numbers[18]);
            }
            
            Poco::Fruit::Component<> getComponentA() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[1])
                .install(getComponentB)
                .addInstanceMultibinding(numbers[4])
                .install(getComponentC)
                .addInstanceMultibinding(numbers[15])
                .install(getComponentC)
                .addInstanceMultibinding(numbers[16]);
            }
    
            Poco::Fruit::Component<> getComponentB() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[2])
                .addInstanceMultibinding(numbers[3]);
            }
    
            Poco::Fruit::Component<> getComponentC() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[5])
                .addInstanceMultibinding(numbers[6])
                .install(getComponentD)
                .addInstanceMultibinding(numbers[11])
                .install(getComponentF)
                .addInstanceMultibinding(numbers[14]);
            }
    
            Poco::Fruit::Component<> getComponentD() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[7])
                .install(getComponentE)
                .addInstanceMultibinding(numbers[10]);
            }
    
            Poco::Fruit::Component<> getComponentE() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[8])
                .addInstanceMultibinding(numbers[9]);
            }
    
            Poco::Fruit::Component<> getComponentF() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[12])
                .addInstanceMultibinding(numbers[13]);
            }
            
            Poco::Fruit::Component<> getRootComponent2() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[19])
                .install(getComponentA2)
                .addInstanceMultibinding(numbers[36])
                .install(getComponentC2)
                .addInstanceMultibinding(numbers[37]);
            }
            
            Poco::Fruit::Component<> getComponentA2() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[20])
                .install(getComponentB2)
                .addInstanceMultibinding(numbers[23])
                .install(getComponentC2)
                .addInstanceMultibinding(numbers[34])
                .install(getComponentC2)
                .addInstanceMultibinding(numbers[35]);
            }
    
            Poco::Fruit::Component<> getComponentB2() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[21])
                .addInstanceMultibinding(numbers[22]);
            }
    
            Poco::Fruit::Component<> getComponentC2() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[24])
                .addInstanceMultibinding(numbers[25])
                .install(getComponentD2)
                .addInstanceMultibinding(numbers[30])
                .install(getComponentF2)
                .addInstanceMultibinding(numbers[33]);
            }
    
            Poco::Fruit::Component<> getComponentD2() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[26])
                .install(getComponentE2)
                .addInstanceMultibinding(numbers[29]);
            }
    
            Poco::Fruit::Component<> getComponentE2() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[27])
                .addInstanceMultibinding(numbers[28]);
            }
    
            Poco::Fruit::Component<> getComponentF2() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[31])
                .addInstanceMultibinding(numbers[32]);
            }        
    
            int main() {
              Poco::Fruit::NormalizedComponent<> normalizedComponent(getRootComponent);
              Poco::Fruit::Injector<> injector(normalizedComponent, getRootComponent2);
              std::vector<int*> result_ptrs = injector.getMultibindings<int>();
              std::vector<int> results;
              std::cout << "Results: ";
              for (int* result : result_ptrs) {
                std::cout << *result << ", ";
                results.push_back(*result);
              }
              std::cout << std::endl;
              Assert(results == numbers);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_with_normalized_component_lazy_components_not_deduped_across(self):
        source = '''
            std::vector<int> numbers = {0, 1, 2, 3, 4};
            
            // *
            // |-- 0
            // |-- A (lazy)
            // |   |-- 1
            // |   `-- 2
            // |-- 3
            // |-- A (lazy, won't be expanded)
            // `-- 4
            
            Poco::Fruit::Component<> getRootComponent();
            Poco::Fruit::Component<> getComponentA();
            
            Poco::Fruit::Component<> getRootComponent() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[0])
                .install(getComponentA)
                .addInstanceMultibinding(numbers[3])
                .install(getComponentA)
                .addInstanceMultibinding(numbers[4]);
            }
            
            Poco::Fruit::Component<> getComponentA() {
              return Poco::Fruit::createComponent()
                .addInstanceMultibinding(numbers[1])
                .addInstanceMultibinding(numbers[2]);
            }
    
            int main() {
              Poco::Fruit::NormalizedComponent<> normalizedComponent(getRootComponent);
              Poco::Fruit::Injector<> injector(normalizedComponent, getRootComponent);
              std::vector<int*> result_ptrs = injector.getMultibindings<int>();
              std::vector<int> results;
              std::cout << "Results: ";
              for (int* result : result_ptrs) {
                std::cout << *result << ", ";
                results.push_back(*result);
              }
              std::cout << std::endl;
              std::vector<int> expected_numbers = {0, 1, 2, 3, 4};
              Assert(results == expected_numbers);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('const X', r'const X'),
        ('X*', r'X\*'),
        ('const X*', r'const X\*'),
        ('std::shared_ptr<X>', r'std::shared_ptr<X>'),
        ('Poco::Fruit::Annotated<Annotation1, const X>', r'const X'),
        ('Poco::Fruit::Annotated<Annotation1, X*>', r'X\*'),
        ('Poco::Fruit::Annotated<Annotation1, const X*>', r'const X\*'),
        ('Poco::Fruit::Annotated<Annotation1, std::shared_ptr<X>>', r'std::shared_ptr<X>'),
    ])
    def test_multibindings_get_error_non_class_type(self, XVariantAnnot, XVariantRegexp):
        source = '''
            void f(Poco::Fruit::Injector<> injector) {
              injector.getMultibindings<XVariantAnnot>();
            }
            '''
        expect_compile_error(
            'NonClassTypeError<XVariantRegexp,X>',
            'A non-class type T was specified. Use C instead.',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X&', 'X&'),
        ('const X&', 'const X&'),
        ('Poco::Fruit::Annotated<Annotation1, X&>', 'X&'),
        ('Poco::Fruit::Annotated<Annotation1, const X&>', 'const X&'),
    ])
    def test_multibindings_get_error_reference_type(self, XVariantAnnot, XVariantRegexp):
        source = '''
            void f(Poco::Fruit::Injector<> injector) {
              injector.getMultibindings<XVariantAnnot>();
            }
            '''
        expect_generic_compile_error(
            'declared as a pointer to a reference of type'
            '|forming pointer to reference type'
            '|Poco::Fruit::Injector<.*>::getMultibindings.: no matching overloaded function found',
            COMMON_DEFINITIONS,
            source,
            locals())

if __name__ == '__main__':
    absltest.main()
