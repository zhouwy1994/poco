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
    using XAnnot1 = Fruit::Annotated<Annotation1, X>;
    '''

class TestRequiredTypes(parameterized.TestCase):

    def test_required_success(self):
        source = '''
            struct X {
                virtual void foo() = 0;
                virtual ~X() = default;
            };
            using XFactory = std::function<std::unique_ptr<X>()>;
            struct Y {
                XFactory xFactory;
    
                INJECT(Y(XFactory xFactory))
                    : xFactory(xFactory) {
                }
    
                void doStuff() {
                    xFactory()->foo();
                }
            };
            Fruit::Component<Fruit::Required<XFactory>, Y> getYComponent() {
                return Fruit::createComponent();
            }
            struct XImpl : public X {
                INJECT(XImpl()) = default;
                void foo() override {}
            };
            Fruit::Component<XFactory> getXFactoryComponent() {
                return Fruit::createComponent()
                    .bind<X, XImpl>();
            }
            Fruit::Component<Y> getComponent() {
                return Fruit::createComponent()
                    .install(getYComponent)
                    .install(getXFactoryComponent);
            }
            int main() {
                Fruit::Injector<Y> injector(getComponent);
                Y* y(injector);
                y->doStuff();
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_required_annotated_success(self):
        source = '''
            struct X {
                virtual void foo() = 0;
                virtual ~X() = default;
            };
            using XFactory = std::function<std::unique_ptr<X>()>;
            using XFactoryAnnot = Fruit::Annotated<Annotation1, XFactory>;
            struct Y {
                XFactory xFactory;
    
                INJECT(Y(ANNOTATED(Annotation1, XFactory) xFactory))
                    : xFactory(xFactory) {
                }
    
                void doStuff() {
                    xFactory()->foo();
                }
            };
            Fruit::Component<Fruit::Required<XFactoryAnnot>, Y> getYComponent() {
                return Fruit::createComponent();
            }
            struct XImpl : public X {
                INJECT(XImpl()) = default;
                void foo() override {}
            };
            Fruit::Component<XFactoryAnnot> getXFactoryComponent() {
                return Fruit::createComponent()
                    .bind<Fruit::Annotated<Annotation1, X>, Fruit::Annotated<Annotation1, XImpl>>();
            }
            Fruit::Component<Y> getComponent() {
                return Fruit::createComponent()
                    .install(getYComponent)
                    .install(getXFactoryComponent);
            }
            int main() {
                Fruit::Injector<Y> injector(getComponent);
                Y* y(injector);
                y->doStuff();
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_required_forward_declared_success(self):
        source = '''
            struct X;
            using XFactory = std::function<std::unique_ptr<X>()>;
            struct Y {
                XFactory xFactory;
    
                INJECT(Y(XFactory xFactory))
                    : xFactory(xFactory) {
                }
    
                void doStuff();
            };
            Fruit::Component<Fruit::Required<XFactory>, Y> getYComponent() {
                return Fruit::createComponent();
            }
            Fruit::Component<XFactory> getXFactoryComponent();
            Fruit::Component<Y> getComponent() {
                return Fruit::createComponent()
                    .install(getYComponent)
                    .install(getXFactoryComponent);
            }
            int main() {
                Fruit::Injector<Y> injector(getComponent);
                Y* y(injector);
                y->doStuff();
            }
    
            // We define X as late as possible, to make sure that all the above compiles even if X is only forward-declared.
            struct X {
                virtual void foo() = 0;
                virtual ~X() = default;
            };
            void Y::doStuff() {
                xFactory()->foo();
            }
            struct XImpl : public X {
                INJECT(XImpl()) = default;
                void foo() override {}
            };
            Fruit::Component<XFactory> getXFactoryComponent() {
                return Fruit::createComponent()
                    .bind<X, XImpl>();
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_required_annotated_forward_declared_success(self):
        source = '''
            struct X;
            using XFactory = std::function<std::unique_ptr<X>()>;
            using XFactoryAnnot = Fruit::Annotated<Annotation1, XFactory>;
            struct Y {
                XFactory xFactory;
    
                INJECT(Y(ANNOTATED(Annotation1, XFactory) xFactory))
                    : xFactory(xFactory) {
                }
    
                void doStuff();
            };
            Fruit::Component<Fruit::Required<XFactoryAnnot>, Y> getYComponent() {
                return Fruit::createComponent();
            }
            Fruit::Component<XFactoryAnnot> getXFactoryComponent();
            Fruit::Component<Y> getComponent() {
                return Fruit::createComponent()
                    .install(getYComponent)
                    .install(getXFactoryComponent);
            }
            int main() {
                Fruit::Injector<Y> injector(getComponent);
                Y* y(injector);
                y->doStuff();
            }
    
            // We define X as late as possible, to make sure that all the above compiles even if X is only forward-declared.
            struct X {
                virtual void foo() = 0;
                virtual ~X() = default;
            };
            void Y::doStuff() {
                xFactory()->foo();
            }
            struct XImpl : public X {
                INJECT(XImpl()) = default;
                void foo() override {}
            };
            Fruit::Component<XFactoryAnnot> getXFactoryComponent() {
                return Fruit::createComponent()
                    .bind<Fruit::Annotated<Annotation1, X>, Fruit::Annotated<Annotation1, XImpl>>();
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_required_const_forward_declared_success(self):
        source = '''
            struct X;
            using XFactory = std::function<std::unique_ptr<X>()>;
            struct Y {
                XFactory xFactory;
    
                INJECT(Y(XFactory xFactory))
                    : xFactory(xFactory) {
                }
    
                void doStuff();
            };
            Fruit::Component<Fruit::Required<const XFactory>, Y> getYComponent() {
                return Fruit::createComponent();
            }
            Fruit::Component<const XFactory> getXFactoryComponent();
            Fruit::Component<Y> getComponent() {
                return Fruit::createComponent()
                    .install(getYComponent)
                    .install(getXFactoryComponent);
            }
            int main() {
                Fruit::Injector<Y> injector(getComponent);
                Y* y(injector);
                y->doStuff();
            }
    
            // We define X as late as possible, to make sure that all the above compiles even if X is only forward-declared.
            struct X {
                virtual void foo() = 0;
                virtual ~X() = default;
            };
            void Y::doStuff() {
                xFactory()->foo();
            }
            struct XImpl : public X {
                INJECT(XImpl()) = default;
                void foo() override {}
            };
            Fruit::Component<const XFactory> getXFactoryComponent() {
                return Fruit::createComponent()
                    .bind<X, XImpl>();
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

    def test_required_const_annotated_forward_declared_success(self):
        source = '''
            struct X;
            using XFactory = std::function<std::unique_ptr<X>()>;
            using ConstXFactoryAnnot = Fruit::Annotated<Annotation1, const XFactory>;
            struct Y {
                XFactory xFactory;
    
                INJECT(Y(ANNOTATED(Annotation1, XFactory) xFactory))
                    : xFactory(xFactory) {
                }
    
                void doStuff();
            };
            Fruit::Component<Fruit::Required<ConstXFactoryAnnot>, Y> getYComponent() {
                return Fruit::createComponent();
            }
            Fruit::Component<ConstXFactoryAnnot> getXFactoryComponent();
            Fruit::Component<Y> getComponent() {
                return Fruit::createComponent()
                    .install(getYComponent)
                    .install(getXFactoryComponent);
            }
            int main() {
                Fruit::Injector<Y> injector(getComponent);
                Y* y(injector);
                y->doStuff();
            }
    
            // We define X as late as possible, to make sure that all the above compiles even if X is only forward-declared.
            struct X {
                virtual void foo() = 0;
                virtual ~X() = default;
            };
            void Y::doStuff() {
                xFactory()->foo();
            }
            struct XImpl : public X {
                INJECT(XImpl()) = default;
                void foo() override {}
            };
            Fruit::Component<ConstXFactoryAnnot> getXFactoryComponent() {
                return Fruit::createComponent()
                    .bind<Fruit::Annotated<Annotation1, X>, Fruit::Annotated<Annotation1, XImpl>>();
            }
            '''
        expect_success(COMMON_DEFINITIONS, source)

if __name__ == '__main__':
    absltest.main()
