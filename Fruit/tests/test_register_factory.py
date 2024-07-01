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
import pytest
from absl.testing import parameterized
from fruit_test_common import *
from fruit_test_config import CXX_COMPILER_NAME

COMMON_DEFINITIONS = '''
    #include "test_common.h"

    struct Scaler;
    struct ScalerImpl;

    struct Annotation1 {};
    using ScalerAnnot1 = Poco::Fruit::Annotated<Annotation1, Scaler>;
    using ScalerImplAnnot1 = Poco::Fruit::Annotated<Annotation1, ScalerImpl>;

    struct Annotation2 {};
    using ScalerAnnot2 = Poco::Fruit::Annotated<Annotation2, Scaler>;
    using ScalerImplAnnot2 = Poco::Fruit::Annotated<Annotation2, ScalerImpl>;
    
    template <typename T>
    using WithNoAnnotation = T;
    
    template <typename T>
    using WithAnnotation1 = Poco::Fruit::Annotated<Annotation1, T>;
    '''

class TestRegisterFactory(parameterized.TestCase):

    @parameterized.parameters([
        'std::function<X()>',
        'Poco::Fruit::Annotated<Annotation1, std::function<X()>>',
    ])
    def test_register_factory_success_no_params_autoinject(self, XFactoryAnnot):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            Poco::Fruit::Component<XFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<XFactoryAnnot> injector(getComponent);
              injector.get<XFactoryAnnot>()();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X()', 'X', 'std::function<X()>'),
        ('X()', 'Poco::Fruit::Annotated<Annotation1, X>', 'Poco::Fruit::Annotated<Annotation1, std::function<X()>>'),
        ('std::unique_ptr<X>()', 'std::unique_ptr<X>', 'std::function<std::unique_ptr<X>()>'),
        ('std::unique_ptr<X>()', 'Poco::Fruit::Annotated<Annotation1, std::unique_ptr<X>>', 'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>'),
    ])
    def test_register_factory_success_no_params(self, ConstructX, XPtrAnnot, XPtrFactoryAnnot):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<XPtrFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<XPtrAnnot()>([](){return ConstructX;});
            }
    
            int main() {
              Poco::Fruit::Injector<XPtrFactoryAnnot> injector(getComponent);
              injector.get<XPtrFactoryAnnot>()();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        '',
        'const',
    ])
    def test_register_factory_autoinject_success(self, MaybeConst):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              INJECT(ScalerImpl(ASSISTED(double) factor))
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<MaybeConst ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImpl>();
            }
    
            int main() {
              Poco::Fruit::Injector<MaybeConst ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_autoinject_abstract_class_with_no_virtual_destructor_error(self):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
            };
    
            struct ScalerImpl : public Scaler {
            public:
              INJECT(ScalerImpl(ASSISTED(double))) {
              }
    
              double scale(double x) override {
                return x;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImpl>();
            }
            '''
        expect_compile_error(
            r'FactoryBindingForUniquePtrOfClassWithNoVirtualDestructorError<std::function<std::unique_ptr<Scaler(,std::default_delete<Scaler>)?>\(double\)>,std::function<std::unique_ptr<ScalerImpl(,std::default_delete<ScalerImpl>)?>\(double\)>>',
            r'Fruit was trying to bind BaseFactory to DerivedFactory but the return type of BaseFactory is a std::unique_ptr of a class with no virtual destructor',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_autoinject_non_abstract_class_with_no_virtual_destructor_error(self):
        source = '''
            struct Scaler {
            };
    
            struct ScalerImpl : public Scaler {
            public:
              INJECT(ScalerImpl(ASSISTED(double))) {
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImpl>();
            }
            '''
        expect_compile_error(
            r'FactoryBindingForUniquePtrOfClassWithNoVirtualDestructorError<std::function<std::unique_ptr<Scaler(,std::default_delete<Scaler>)?>\(double\)>,std::function<std::unique_ptr<ScalerImpl(,std::default_delete<ScalerImpl>)?>\(double\)>>',
            r'Fruit was trying to bind BaseFactory to DerivedFactory but the return type of BaseFactory is a std::unique_ptr of a class with no virtual destructor',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Scaler',
         'std::function<std::unique_ptr<Scaler>(double)>',
         'std::function<std::unique_ptr<Scaler>(double)>'),
        ('Scaler',
         'std::function<std::unique_ptr<Scaler>(double)>',
         'const std::function<std::unique_ptr<Scaler>(double)>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>',
         'Poco::Fruit::Annotated<Annotation1, const std::function<std::unique_ptr<Scaler>(double)>>'),
    ])
    def test_autoinject(self, ScalerAnnot, ScalerFactoryAnnot, MaybeConstScalerFactoryAnnot):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              INJECT(ScalerImpl(ASSISTED(double) factor))
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<MaybeConstScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot, ScalerImpl>();
            }
    
            int main() {
              Poco::Fruit::Injector<MaybeConstScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        '',
        'const',
    ])
    def test_autoinject_returning_value(self, MaybeConst):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            struct Scaler {
            private:
              double factor;
    
            public:
              INJECT(Scaler(ASSISTED(double) factor, X))
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<MaybeConst ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<MaybeConst ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Scaler',
         'ScalerImpl',
         'std::function<std::unique_ptr<Scaler>(double)>',
         r'std::function<std::unique_ptr<ScalerImpl(,std::default_delete<ScalerImpl>)?>\(double\)>',
         ),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>',
         r'Poco::Fruit::Annotated<Annotation2,std::function<std::unique_ptr<ScalerImpl(,std::default_delete<ScalerImpl>)?>\(double\)>>',
         ),
    ])
    def test_autoinject_error_abstract_class(self, ScalerAnnot, ScalerImplAnnot, ScalerFactoryAnnot, ScalerImplFactoryAnnotRegex):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              // Note: here we "forgot" to implement scale() (on purpose, for this test) so ScalerImpl is an abstract class.
            };
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot, ScalerImplAnnot>();
            }
            '''
        expect_compile_error(
            'NoBindingFoundForAbstractClassError<ScalerImplFactoryAnnotRegex,ScalerImpl>',
            'No explicit binding was found for T, and note that C is an abstract class',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_autoinject_nonmovable_ok(self):
        source = '''
            struct I {
              virtual ~I() = default;
            };
    
            struct C : public I {
              INJECT(C()) = default;
    
              C(const C&) = delete;
              C(C&&) = delete;
              C& operator=(const C&) = delete;
              C& operator=(C&&) = delete;
            };
    
            using IFactory = std::function<std::unique_ptr<I>()>;
    
            Poco::Fruit::Component<IFactory> getIFactory() {
              return Poco::Fruit::createComponent()
                  .bind<I, C>();
            }
    
            int main() {
              Poco::Fruit::Injector<IFactory> injector(getIFactory);
              IFactory iFactory(injector);
              std::unique_ptr<I> i = iFactory();
              (void)i;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_moveonly_ref(self):
        source = '''
            struct Bar {
              Bar() = default;
    
              Bar(const Bar&) = delete;
              Bar(Bar&&) = default;
              Bar& operator=(const Bar&) = delete;
              Bar& operator=(Bar&&) = default;
            };
    
            struct Foo {
              Foo(Bar&& bar) {
                Bar b(std::move(bar));
                (void)b;
              }
            };
    
            using FooFactory = std::function<Foo(Bar&&)>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              return Poco::Fruit::createComponent()
                  .registerFactory<Foo(Poco::Fruit::Assisted<Bar&&>)>(
                      [](Bar&& bar) {
                        return Foo(std::move(bar));
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              Foo foo = fooFactory(Bar());
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_nonmovable_ref(self):
        source = '''
            struct Bar {
              Bar() = default;
    
              Bar(const Bar&) = delete;
              Bar(Bar&&) = delete;
              Bar& operator=(const Bar&) = delete;
              Bar& operator=(Bar&&) = delete;
            };
    
            struct Foo {
              Foo(Bar& bar) {
                (void)bar;
              }
            };
    
            using FooFactory = std::function<Foo(Bar&)>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              return Poco::Fruit::createComponent()
                  .registerFactory<Foo(Poco::Fruit::Assisted<Bar&>)>(
                      [](Bar& bar) {
                        return Foo(bar);
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              Bar bar;
              Foo foo = fooFactory(bar);
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_2_assisted_params(self):
        source = '''
            struct Foo {
              Foo(int x, float y) {
                (void)x;
                (void)y;
              }
            };
    
            using FooFactory = std::function<Foo(int, float)>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              return Poco::Fruit::createComponent()
                  .registerFactory<Foo(Poco::Fruit::Assisted<int>, Poco::Fruit::Assisted<float>)>(
                      [](int x, float y) {
                        return Foo(x, y);
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              Foo foo = fooFactory(1, 2.3f);
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_assisted_params_ref(self):
        source = '''
            struct Foo {
              Foo(int x, float y, char z) {
                (void)x;
                (void)y;
                (void)z;
              }
            };
    
            using FooFactory = std::function<Foo(int&, float&&, char)>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              return Poco::Fruit::createComponent()
                  .registerFactory<Foo(Poco::Fruit::Assisted<int&>, Poco::Fruit::Assisted<float&&>, Poco::Fruit::Assisted<char>)>(
                      [](int& x, float&& y, char z) {
                        return Foo(x, std::move(y), z);
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              int x = 1;
              Foo foo = fooFactory(x, 2.3f, 'z');
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_2_assisted_params_returning_value(self):
        source = '''
            struct Foo {
              Foo(int x, float y) {
                (void)x;
                (void)y;
              }
            };
    
            using FooFactory = std::function<Foo(int, float)>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              return Poco::Fruit::createComponent()
                  .registerFactory<Foo(Poco::Fruit::Assisted<int>, Poco::Fruit::Assisted<float>)>(
                      [](int x, float y) {
                        return Foo(x, y);
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              Foo foo = fooFactory(1, 2.3f);
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_instances_bound_to_assisted_params(self):
        source = '''
            struct X {};
            struct Y {};
    
            struct Foo {
              Foo(X x, Y y) {
                (void)x;
                (void)y;
              }
            };
    
            using FooFactory = std::function<Foo()>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              static X x = X();
              static Y y = Y();
              return Poco::Fruit::createComponent()
                  .bindInstance(x)
                  .bindInstance(y)
                  .registerFactory<Foo(X, Y)>(
                      [](X x, Y y) {
                        return Foo(x, y);
                      });
            }
    
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              Foo foo = fooFactory();
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_2_assisted_params_plus_nonassisted_params(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            struct Foo {
              Foo(X, Y, int, float, Z) {
              }
            };
    
            using FooPtrFactory = std::function<std::unique_ptr<Foo>(int, float)>;
    
            Poco::Fruit::Component<FooPtrFactory> getComponent() {
              static X x = X();
              static Y y = Y();
              static Z z = Z();
              return Poco::Fruit::createComponent()
                  .bindInstance(x)
                  .bindInstance(y)
                  .bindInstance(z)
                  .registerFactory<std::unique_ptr<Foo>(X, Y, Poco::Fruit::Assisted<int>, Poco::Fruit::Assisted<float>, Z)>(
                      [](X x, Y y, int n, float a, Z z) {
                        return std::unique_ptr<Foo>(new Foo(x, y, n, a, z));
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooPtrFactory> injector(getComponent);
              FooPtrFactory fooPtrFactory(injector);
              std::unique_ptr<Foo> foo = fooPtrFactory(1, 3.4f);
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_2_assisted_params_plus_nonassisted_params_returning_value(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            struct Foo {
              Foo(X, Y, int, float, Z) {
              }
            };
    
            using FooFactory = std::function<Foo(int, float)>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              static X x = X();
              static Y y = Y();
              static Z z = Z();
              return Poco::Fruit::createComponent()
                  .bindInstance(x)
                  .bindInstance(y)
                  .bindInstance(z)
                  .registerFactory<Foo(X, Y, Poco::Fruit::Assisted<int>, Poco::Fruit::Assisted<float>, Z)>(
                      [](X x, Y y, int n, float a, Z z) {
                        return Foo(x, y, n, a, z);
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              Foo foo = fooFactory(1, 3.4f);
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_mixed_assisted_and_injected_params(self):
        source = '''
            struct X {};
            struct Y {};
    
            struct Foo {
              Foo(int, float, X, Y, double) {
              }
            };
    
            using FooFactory = std::function<Foo(int, float, double)>;
    
            Poco::Fruit::Component<FooFactory> getComponent() {
              static X x = X();
              static Y y = Y();
              return Poco::Fruit::createComponent()
                  .bindInstance(x)
                  .bindInstance(y)
                  .registerFactory<Foo(Poco::Fruit::Assisted<int>, Poco::Fruit::Assisted<float>, X, Y, Poco::Fruit::Assisted<double>)>(
                      [](int n, float a, X x, Y y, double d) {
                        return Foo(n, a, x, y, d);
                      });
            }
    
            int main() {
              Poco::Fruit::Injector<FooFactory> injector(getComponent);
              FooFactory fooFactory(injector);
              Foo foo = fooFactory(1, 3.4f, 3.456);
              (void)foo;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_annotation_in_signature_return_type(self):
        source = '''
            struct X {
              using Inject = Poco::Fruit::Annotated<Annotation1, X>();
            };
    
            Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'InjectTypedefWithAnnotationError<X>',
            'C::Inject is a signature that returns an annotated type',
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_annotation_in_signature_return_type_returning_value(self):
        source = '''
            struct X {
              using Inject = Poco::Fruit::Annotated<Annotation1, X>();
            };
    
            Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation1, std::function<X()>>> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'InjectTypedefWithAnnotationError<X>',
            'C::Inject is a signature that returns an annotated type',
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_from_provider_simple(self):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor, X)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerProvider([](X x) {
                  return std::function<std::unique_ptr<ScalerImpl>(double)>([x](double n){
                    return std::unique_ptr<ScalerImpl>(new ScalerImpl(n, x));
                  });
                })
                .bind<Scaler, ScalerImpl>();
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('Scaler',
         'std::function<std::unique_ptr<Scaler>(double)>',
         'std::function<std::unique_ptr<Scaler>(double)>',
         'ScalerImpl',
         'std::function<std::unique_ptr<ScalerImpl>(double)>'),
        ('Scaler',
         'std::function<std::unique_ptr<Scaler>(double)>',
         'const std::function<std::unique_ptr<Scaler>(double)>',
         'ScalerImpl',
         'std::function<std::unique_ptr<ScalerImpl>(double)>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation2, std::function<std::unique_ptr<ScalerImpl>(double)>>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>',
         'Poco::Fruit::Annotated<Annotation1, const std::function<std::unique_ptr<Scaler>(double)>>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation2, std::function<std::unique_ptr<ScalerImpl>(double)>>'),
    ])
    def test_autoinject_from_provider(self, ScalerAnnot, ScalerFactoryAnnot, MaybeConstScalerFactoryAnnot, ScalerImplAnnot, ScalerImplFactoryAnnot):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor, X)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
            using ScalerImplFactory = std::function<std::unique_ptr<ScalerImpl>(double)>;
    
            Poco::Fruit::Component<MaybeConstScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerProvider<ScalerImplFactoryAnnot(X)>([](X x) {
                  return std::function<std::unique_ptr<ScalerImpl>(double)>([x](double n){
                    return std::unique_ptr<ScalerImpl>(new ScalerImpl(n, x));
                  });
                })
                .bind<ScalerAnnot, ScalerImplAnnot>();
            }
    
            int main() {
              Poco::Fruit::Injector<MaybeConstScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'ScalerFactory',
        'Poco::Fruit::Annotated<Annotation1, ScalerFactory>',
    ])
    def test_autoinject_from_provider_returning_value(self, ScalerFactoryAnnot):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            struct Scaler {
            private:
              double factor;
    
            public:
              Scaler(double factor, X)
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerProvider<ScalerFactoryAnnot(X)>([](X x) {
                  return std::function<Scaler(double)>([x](double n){
                    return Scaler(n, x);
                  });
                });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        '',
        'const',
    ], [
        'X',
        'ANNOTATED(Annotation1, X)',
    ])
    def test_autoinject_with_binding(self, MaybeConst, X_ANNOT):
        source = '''
            struct X {
              using Inject = X();
            };
    
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              INJECT(ScalerImpl(ASSISTED(double) factor, X_ANNOT x))
                : factor(factor) {
                  (void)x;
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<MaybeConst ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImpl>();
            }
    
            int main() {
              Poco::Fruit::Injector<MaybeConst ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        '',
        'const',
    ], [
        'X',
        'ANNOTATED(Annotation1, X)',
    ])
    def test_autoinject_with_binding_returning_value(self, MaybeConst, X_ANNOT):
        source = '''
            struct X {
              using Inject = X();
            };
    
            struct Scaler {
            private:
              double factor;
    
            public:
              INJECT(Scaler(ASSISTED(double) factor, X_ANNOT x))
                : factor(factor) {
                  (void)x;
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<MaybeConst ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<MaybeConst ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_autoinject_with_binding_variant(self):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              INJECT(ScalerImpl(X, ASSISTED(double) factor))
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImpl>();
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_autoinject_with_binding_variant_returning_value(self):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            struct Scaler {
            private:
              double factor;
    
            public:
              INJECT(Scaler(X, ASSISTED(double) factor))
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('Scaler',
         'ScalerImpl',
         'std::function<std::unique_ptr<Scaler>(double)>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>'),
    ])
    def test_register_factory_success(self, ScalerAnnot, ScalerImplAnnot, ScalerFactoryAnnot):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot, ScalerImplAnnot>()
                .registerFactory<ScalerImplAnnot(Poco::Fruit::Assisted<double>)>([](double factor) { return ScalerImpl(factor); });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_with_annotation_returning_value(self):
        source = '''
            struct Scaler {
            private:
              double factor;
    
            public:
              Scaler(double factor)
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
            using ScalerFactoryAnnot1 = Poco::Fruit::Annotated<Annotation1, ScalerFactory>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot1> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<ScalerAnnot1(Poco::Fruit::Assisted<double>)>(
                  [](double factor) {
                      return Scaler(factor);
                  });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot1> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot1>();
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_register_factory_with_different_annotation(self):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
            using ScalerFactoryAnnot1 = Poco::Fruit::Annotated<Annotation1, ScalerFactory>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot1> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot1, ScalerImplAnnot2>()
                .registerFactory<ScalerImplAnnot2(Poco::Fruit::Assisted<double>)>(
                    [](double factor) {
                        return ScalerImpl(factor);
                    });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot1> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot1>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)


    @parameterized.parameters([
        ('Scaler',
         'ScalerImpl',
         'std::function<std::unique_ptr<Scaler>(double, double)>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double, double)>>'),
    ])
    def test_register_factory_2arg_success(self, ScalerAnnot, ScalerImplAnnot, ScalerFactoryAnnot):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double, double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot, ScalerImplAnnot>()
                .registerFactory<ScalerImplAnnot(Poco::Fruit::Assisted<double>, Poco::Fruit::Assisted<double>)>(
                    [](double factor, double) { 
                        return ScalerImpl(factor);
                    });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1, 34.2);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_with_different_annotation_error(self):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
            using ScalerFactoryAnnot1 = Poco::Fruit::Annotated<Annotation1, ScalerFactory>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot1> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot1, ScalerImplAnnot1>()
                .registerFactory<ScalerImplAnnot2(Poco::Fruit::Assisted<double>)>([](double factor) { return ScalerImpl(factor); });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot1> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot1>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_compile_error(
            r'NoBindingFoundError<Poco::Fruit::Annotated<Annotation1,std::function<std::unique_ptr<ScalerImpl(,std::default_delete<ScalerImpl>)?>\(double\)>>>',
            r'',
            COMMON_DEFINITIONS,
            source)


    def test_register_factory_dep_on_provider(self):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImpl>()
                .registerProvider([](){return 23;})
                .registerFactory<ScalerImpl(Poco::Fruit::Assisted<double>, Poco::Fruit::Provider<int>)>(
                    [](double factor, Poco::Fruit::Provider<int> provider) {
                        return ScalerImpl(factor * provider.get<int>());
                    });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_register_factory_dep_on_provider_returning_value(self):
        source = '''
            struct Scaler {
            private:
              double factor;
    
            public:
              Scaler(double factor)
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerProvider([](){return 23;})
                .registerFactory<Scaler(Poco::Fruit::Assisted<double>, Poco::Fruit::Provider<int>)>(
                    [](double factor, Poco::Fruit::Provider<int> provider) {
                        return Scaler(factor * provider.get<int>());
                    });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    def test_register_factory_error_abstract_class(self):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              // Note: here we "forgot" to implement scale() (on purpose, for this test) so ScalerImpl is an abstract class.
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImpl>()
                .registerFactory<Poco::Fruit::Annotated<Annotation1, ScalerImpl>(Poco::Fruit::Assisted<double>)>([](double) { return (ScalerImpl*)nullptr; });
            }
            '''
        expect_compile_error(
            'CannotConstructAbstractClassError<ScalerImpl>',
            'The specified class can.t be constructed because it.s an abstract class.',
            COMMON_DEFINITIONS,
            source)

    def test_register_factory_error_not_function(self):
        source = '''
            struct X {
              X(int) {}
            };
    
            Poco::Fruit::Component<std::function<X()>> getComponent() {
              int n = 3;
              return Poco::Fruit::createComponent()
                .registerFactory<X()>([=]{return X(n);});
            }
            '''
        expect_compile_error(
            'LambdaWithCapturesError<.*>',
            'Only lambdas with no captures are supported',
            COMMON_DEFINITIONS,
            source)

    @parameterized.parameters([
        ('Scaler',
         'ScalerImpl',
         'ScalerImpl*',
         'std::function<std::unique_ptr<Scaler>(double)>',
         r'ScalerImpl\*\(Poco::Fruit::Assisted<double>\)'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl*>',
         'Poco::Fruit::Annotated<Annotation2, std::function<std::unique_ptr<Scaler>(double)>>',
         r'Poco::Fruit::Annotated<Annotation2,ScalerImpl\*>\(Poco::Fruit::Assisted<double>\)')
    ])
    def test_register_factory_for_pointer(self, ScalerAnnot, ScalerImplAnnot, ScalerImplPtrAnnot, ScalerFactoryAnnot, ScalerImplFactorySignatureAnnotRegex):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot, ScalerImplAnnot>()
                .registerFactory<ScalerImplPtrAnnot(Poco::Fruit::Assisted<double>)>([](double factor) { return new ScalerImpl(factor); });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_compile_error(
            'FactoryReturningPointerError<ScalerImplFactorySignatureAnnotRegex>',
            'The specified factory returns a pointer. This is not supported',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Scaler*',
         'std::function<Scaler(double)>',
         r'Scaler\*\(Poco::Fruit::Assisted<double>\)'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler*>',
         'Poco::Fruit::Annotated<Annotation1, std::function<Scaler(double)>>',
         r'Poco::Fruit::Annotated<Annotation1,Scaler\*>\(Poco::Fruit::Assisted<double>\)'),
    ])
    def test_register_factory_for_pointer_returning_value(self, ScalerPtrAnnot, ScalerFactoryAnnot, ScalerFactorySignatureAnnotRegex):
        source = '''
            struct Scaler {
            private:
              double factor;
    
            public:
              Scaler(double factor)
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<ScalerPtrAnnot(Poco::Fruit::Assisted<double>)>([](double factor) { return new Scaler(factor); });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_compile_error(
            'FactoryReturningPointerError<ScalerFactorySignatureAnnotRegex>',
            'The specified factory returns a pointer. This is not supported',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Scaler',
         'ScalerImpl',
         'std::unique_ptr<ScalerImpl>',
         'std::function<std::unique_ptr<Scaler>(double)>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation2, std::unique_ptr<ScalerImpl>>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>'),
    ])
    def test_register_factory_for_unique_pointer(self, ScalerAnnot, ScalerImplAnnot, ScalerImplPtrAnnot, ScalerFactoryAnnot):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot, ScalerImplAnnot>()
                .registerFactory<ScalerImplPtrAnnot(Poco::Fruit::Assisted<double>)>(
                    [](double factor) {
                        return std::unique_ptr<ScalerImpl>(new ScalerImpl(factor));
                    });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Scaler',
         'ScalerImpl',
         'std::unique_ptr<ScalerImpl>',
         'std::function<std::unique_ptr<Scaler>(double)>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation2, ScalerImpl>',
         'Poco::Fruit::Annotated<Annotation2, std::unique_ptr<ScalerImpl>>',
         'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<Scaler>(double)>>'),
    ])
    def test_register_factory_for_unique_pointer_returning_invalid_unique_ptr_ok(self, ScalerAnnot, ScalerImplAnnot, ScalerImplPtrAnnot, ScalerFactoryAnnot):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
              virtual ~Scaler() = default;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<ScalerAnnot, ScalerImplAnnot>()
                .registerFactory<ScalerImplPtrAnnot(Poco::Fruit::Assisted<double>)>(
                    [](double) {
                        return std::unique_ptr<ScalerImpl>(nullptr);
                    });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              Assert(scaler.get() == nullptr);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('Scaler',
         'std::function<Scaler(double)>'),
        ('Poco::Fruit::Annotated<Annotation1, Scaler>',
         'Poco::Fruit::Annotated<Annotation1, std::function<Scaler(double)>>'),
    ])
    def test_register_factory_for_unique_pointer_returning_value(self, ScalerAnnot, ScalerFactoryAnnot):
        source = '''
            struct Scaler {
            private:
              double factor;
    
            public:
              Scaler(double factor)
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<ScalerFactoryAnnot> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<ScalerAnnot(Poco::Fruit::Assisted<double>)>(
                    [](double factor) {
                        return Scaler(factor);
                    });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactoryAnnot> injector(getScalerComponent);
              ScalerFactory scalerFactory = injector.get<ScalerFactoryAnnot>();
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'ScalerImpl',
        'Poco::Fruit::Annotated<Annotation1, ScalerImpl>',
    ])
    def test_register_factory_inconsistent_signature(self, ScalerImplAnnot):
        source = '''
            struct Scaler {
              virtual double scale(double x) = 0;
            };
    
            struct ScalerImpl : public Scaler {
            private:
              double factor;
    
            public:
              ScalerImpl(double factor)
                : factor(factor) {
              }
    
              double scale(double x) override {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<std::unique_ptr<Scaler>(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .bind<Scaler, ScalerImplAnnot>()
                .registerFactory<ScalerImplAnnot(Poco::Fruit::Assisted<double>)>([](float factor) { return ScalerImpl(factor); });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              std::unique_ptr<Scaler> scaler = scalerFactory(12.1);
              std::cout << scaler->scale(3) << std::endl;
            }
            '''
        expect_compile_error(
            r'FunctorSignatureDoesNotMatchError<ScalerImpl\(double\),ScalerImpl\(float\)>',
            r'Unexpected functor signature',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_inconsistent_signature_returning_value(self):
        source = '''
            struct Scaler {
            private:
              double factor;
    
            public:
              Scaler(double factor)
                : factor(factor) {
              }
    
              double scale(double x) {
                return x * factor;
              }
            };
    
            using ScalerFactory = std::function<Scaler(double)>;
    
            Poco::Fruit::Component<ScalerFactory> getScalerComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<Scaler(Poco::Fruit::Assisted<double>)>([](float factor) { return Scaler(factor); });
            }
    
            int main() {
              Poco::Fruit::Injector<ScalerFactory> injector(getScalerComponent);
              ScalerFactory scalerFactory(injector);
              Scaler scaler = scalerFactory(12.1);
              std::cout << scaler.scale(3) << std::endl;
            }
            '''
        expect_compile_error(
            r'FunctorSignatureDoesNotMatchError<Scaler\(double\),Scaler\(float\)>',
            r'Unexpected functor signature',
            COMMON_DEFINITIONS,
            source)

    def test_register_factory_nonmovable_ok(self):
        source = '''
            struct C {
              INJECT(C()) = default;
    
              C(const C&) = delete;
              C(C&&) = delete;
              C& operator=(const C&) = delete;
              C& operator=(C&&) = delete;
            };
    
            using CFactory = std::function<std::unique_ptr<C>()>;
    
            Poco::Fruit::Component<CFactory> getCFactory() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<CFactory> injector(getCFactory);
              CFactory cFactory(injector);
              std::unique_ptr<C> c = cFactory();
              (void)c;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

    # TODO: this might not be the best error message, maybe we should ignore the constructor entirely in the message,
    # or mention that there are other ways to satisfy that dependency.
    @parameterized.parameters([
        ('X',
         'std::function<X(int)>'),
        ('Poco::Fruit::Annotated<Annotation1, X>',
         'Poco::Fruit::Annotated<Annotation1, std::function<X(int)>>'),
    ])
    def test_register_factory_not_existing_constructor1(self, XAnnot, XFactoryAnnot):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
    
            Poco::Fruit::Component<XFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            r'FunctorSignatureDoesNotMatchError<XAnnot\(int\),XAnnot\((void)?\)>',
            r'Unexpected functor signature',
            COMMON_DEFINITIONS,
            source,
            locals())

    # TODO: this might not be the best error message, maybe we should ignore the constructor entirely in the message,
    # or mention that there are other ways to satisfy that dependency.
    @parameterized.parameters([
        ('std::function<std::unique_ptr<X>(int)>',
         r'std::unique_ptr<X(,std::default_delete<X>)?>\(int\)',
         r'std::unique_ptr<X(,std::default_delete<X>)?>\((void)?\)'),
        ('Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>(int)>>',
         r'Poco::Fruit::Annotated<Annotation1,std::unique_ptr<X(,std::default_delete<X>)?>>\(int\)',
         r'Poco::Fruit::Annotated<Annotation1,std::unique_ptr<X(,std::default_delete<X>)?>>\((void)?\)')
    ])
    def test_register_factory_not_existing_constructor2(self, XIntFactoryAnnot, XIntFactoryAnnotRegex, XVoidFactoryAnnotRegex):
        source = '''
            struct X {
              using Inject = X();
            };
    
            Poco::Fruit::Component<XIntFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'FunctorSignatureDoesNotMatchError<XIntFactoryAnnotRegex,XVoidFactoryAnnotRegex>',
            'Unexpected functor signature',
            COMMON_DEFINITIONS,
            source,
            locals())

    # TODO: this might not be the best error message, maybe we should ignore the constructor entirely in the message,
    # or mention that there are other ways to satisfy that dependency.
    @parameterized.parameters([
        ('X',
         'std::function<X(int)>'),
        ('Poco::Fruit::Annotated<Annotation1, X>',
         'Poco::Fruit::Annotated<Annotation1, std::function<X(int)>>'),
    ])
    def test_register_factory_not_existing_constructor2_returning_value(self, XAnnot, XFactoryAnnot):
        source = '''
            struct X {
              using Inject = X();
            };
    
            Poco::Fruit::Component<XFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            r'FunctorSignatureDoesNotMatchError<XAnnot\(int\), XAnnot\((void)?\)>',
            r'Unexpected functor signature',
            COMMON_DEFINITIONS,
            source,
            locals())


    @parameterized.parameters([
        'std::function<X()>',
        'Poco::Fruit::Annotated<Annotation1, std::function<X()>>',
    ])
    def test_register_factory_success_factory_movable_only_implicit(self, XFactoryAnnot):
        source = '''
            struct X {
              INJECT(X()) = default;
              X(X&&) = default;
              X(const X&) = delete;
            };
    
            Poco::Fruit::Component<XFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<XFactoryAnnot> injector(getComponent);
              injector.get<XFactoryAnnot>()();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'X()', 'std::function<X()>'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'X()', 'Poco::Fruit::Annotated<Annotation1, std::function<X()>>'),
        ('std::unique_ptr<X>', 'std::unique_ptr<X>(new X())', 'std::function<std::unique_ptr<X>()>'),
        ('Poco::Fruit::Annotated<Annotation1, std::unique_ptr<X>>', 'std::unique_ptr<X>(new X())', 'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>'),
    ])
    def test_register_factory_success_factory_movable_only_explicit(self, XPtrAnnot, ConstructX, XPtrFactoryAnnot):
        source = '''
            struct X {
              X() = default;
              X(X&&) = default;
              X(const X&) = delete;
            };
    
            Poco::Fruit::Component<XPtrFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<XPtrAnnot()>([](){return ConstructX;});
            }
    
            int main() {
              Poco::Fruit::Injector<XPtrFactoryAnnot> injector(getComponent);
              injector.get<XPtrFactoryAnnot>()();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'std::function<std::unique_ptr<X>()>',
        'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>',
    ])
    def test_register_factory_success_factory_not_movable_implicit(self, XPtrFactoryAnnot):
        source = '''
            struct X {
              INJECT(X()) = default;
              X(X&&) = delete;
              X(const X&) = delete;
            };
    
            Poco::Fruit::Component<XPtrFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent();
            }
    
            int main() {
              Poco::Fruit::Injector<XPtrFactoryAnnot> injector(getComponent);
              injector.get<XPtrFactoryAnnot>()();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('std::unique_ptr<X>', 'std::function<std::unique_ptr<X>()>'),
        ('Poco::Fruit::Annotated<Annotation1, std::unique_ptr<X>>', 'Poco::Fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>'),
    ])
    def test_register_factory_success_factory_not_movable_explicit_returning_pointer(self, XPtrAnnot, XPtrFactoryAnnot):
        source = '''
            struct X {
              X() = default;
              X(X&&) = delete;
              X(const X&) = delete;
            };
    
            Poco::Fruit::Component<XPtrFactoryAnnot> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<XPtrAnnot()>([](){return std::unique_ptr<X>(new X());});
            }
    
            int main() {
              Poco::Fruit::Injector<XPtrFactoryAnnot> injector(getComponent);
              injector.get<XPtrFactoryAnnot>()();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('std::unique_ptr<X>(new X())', 'std::unique_ptr<X>'),
    ], [
        'WithNoAnnotation',
        'WithAnnotation1',
    ], [
        'Y',
        'Y*',
        'const Y*',
        'Y&',
        'const Y&',
        'std::shared_ptr<Y>',
        'Poco::Fruit::Provider<Y>',
        'Poco::Fruit::Provider<const Y>',
    ])
    def test_register_factory_with_param_success(self, ConstructX, XPtr, WithAnnot, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            Poco::Fruit::Component<WithAnnot<Y>> getYComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<WithAnnot<Y>()>();
            }
    
            Poco::Fruit::Component<std::function<XPtr()>> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getYComponent)
                .registerFactory<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; });
            }
    
            int main() {
              Poco::Fruit::Injector<std::function<XPtr()>> injector(getComponent);
              XPtr x = injector.get<std::function<XPtr()>>()();
              (void) x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('std::unique_ptr<X>(new X())', 'std::unique_ptr<X>'),
    ], [
        'WithNoAnnotation',
        'WithAnnotation1',
    ], [
        'Y',
        'const Y*',
        'const Y&',
        'Poco::Fruit::Provider<const Y>',
    ])
    def test_register_factory_with_param_const_binding_success(self, ConstructX, XPtr, WithAnnot, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            const Y y{};
            
            Poco::Fruit::Component<WithAnnot<const Y>> getYComponent() {
              return Poco::Fruit::createComponent()
                .bindInstance<WithAnnot<Y>, Y>(y);
            }
    
            Poco::Fruit::Component<std::function<XPtr()>> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getYComponent)
                .registerFactory<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; });
            }
    
            int main() {
              Poco::Fruit::Injector<std::function<XPtr()>> injector(getComponent);
              XPtr x = injector.get<std::function<XPtr()>>()();
              (void) x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('std::unique_ptr<X>(new X())', 'std::unique_ptr<X>'),
    ], [
        ('WithNoAnnotation', 'Y'),
        ('WithAnnotation1', 'Poco::Fruit::Annotated<Annotation1, Y>'),
    ], [
        'X',
        'std::unique_ptr<X>',
    ], [
        'Y*',
        'Y&',
        'std::shared_ptr<Y>',
        'Poco::Fruit::Provider<Y>',
    ])
    def test_register_factory_with_param_error_nonconst_param_required(self, ConstructX, XPtr, WithAnnot, YAnnotRegex, XFactoryResult, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            Poco::Fruit::Component<WithAnnot<const Y>> getYComponent();
    
            Poco::Fruit::Component<std::function<XFactoryResult()>> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getYComponent)
                .registerFactory<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; });
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
        ('std::unique_ptr<X>(new X())', 'std::unique_ptr<X>'),
    ], [
        'X',
        'std::unique_ptr<X>',
    ], [
        ('WithNoAnnotation', 'Y'),
        ('WithAnnotation1', 'Poco::Fruit::Annotated<Annotation1, Y>'),
    ], [
        'Y*',
        'Y&',
        'std::shared_ptr<Y>',
        'Poco::Fruit::Provider<Y>',
    ])
    def test_register_factory_with_param_error_nonconst_param_required_install_after(self, ConstructX, XPtr, XFactoryResult, WithAnnot, YAnnotRegex, YVariant):
        source = '''
            struct Y {};
            struct X {};
            
            Poco::Fruit::Component<WithAnnot<const Y>> getYComponent();
    
            Poco::Fruit::Component<std::function<XFactoryResult()>> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<XPtr(WithAnnot<YVariant>)>([](YVariant){ return ConstructX; })
                .install(getYComponent);
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
        ('std::unique_ptr<X>(new X())', 'std::unique_ptr<X>'),
    ], [
        'WithNoAnnotation',
        'WithAnnotation1',
    ])
    def test_register_factory_with_non_assignable_injected_param_success(self, ConstructX, XPtr, WithAnnot):
        source = '''
            struct Y {
              Y(const Y&) = delete;
              Y& operator=(const Y&) = delete;
              
              Y() = default;
              Y(Y&&) = default;
              Y& operator=(Y&&) = default;              
            };
            struct X {};
            
            Poco::Fruit::Component<WithAnnot<Y>> getYComponent() {
              return Poco::Fruit::createComponent()
                .registerConstructor<WithAnnot<Y>()>();
            }
    
            Poco::Fruit::Component<std::function<XPtr()>> getComponent() {
              return Poco::Fruit::createComponent()
                .install(getYComponent)
                .registerFactory<XPtr(WithAnnot<Y&>)>([](Y&){ return ConstructX; });
            }
    
            int main() {
              Poco::Fruit::Injector<std::function<XPtr()>> injector(getComponent);
              XPtr x = injector.get<std::function<XPtr()>>()();
              (void) x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @multiple_parameters([
        ('X()', 'X'),
        ('std::unique_ptr<X>(new X())', 'std::unique_ptr<X>'),
    ])
    def test_register_factory_with_non_assignable_assisted_param_success(self, ConstructX, XPtr):
        source = '''
            struct Y {
              Y(const Y&) = delete;
              Y& operator=(const Y&) = delete;
              
              Y() = default;
              Y(Y&&) = default;
              Y& operator=(Y&&) = default;              
            };
            struct X {};
            
            Poco::Fruit::Component<std::function<XPtr(Y)>> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<XPtr(Poco::Fruit::Assisted<Y>)>([](Y){ return ConstructX; });
            }
    
            int main() {
              Poco::Fruit::Injector<std::function<XPtr(Y)>> injector(getComponent);
              XPtr x = injector.get<std::function<XPtr(Y)>>()(Y());
              (void) x;
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_requiring_nonconst_then_requiring_const_ok(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<std::function<Y()>, std::function<Z()>> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<Y(X&)>([](X&) { return Y();})
                .registerFactory<Z(const X&)>([](const X&) { return Z();})
                .registerConstructor<X()>();
            }
            
            int main() {
              Poco::Fruit::Injector<std::function<Y()>, std::function<Z()>> injector(getRootComponent);
              std::function<Y()> yFactory = injector.get<std::function<Y()>>();
              yFactory();
              std::function<Z()> zFactory = injector.get<std::function<Z()>>();
              zFactory();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_requiring_nonconst_then_requiring_const_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, std::function<Y()>, std::function<Z()>> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<Y(X&)>([](X&) { return Y();})
                .registerFactory<Z(const X&)>([](const X&) { return Z();});
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_requiring_const_then_requiring_nonconst_ok(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<std::function<Y()>, std::function<Z()>> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<Y(const X&)>([](const X&) { return Y();})
                .registerFactory<Z(X&)>([](X&) { return Z();})
                .registerConstructor<X()>();
            }
            
            int main() {
              Poco::Fruit::Injector<std::function<Y()>, std::function<Z()>> injector(getRootComponent);
              std::function<Y()> yFactory = injector.get<std::function<Y()>>();
              yFactory();
              std::function<Z()> zFactory = injector.get<std::function<Z()>>();
              zFactory();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_requiring_const_then_requiring_nonconst_declaring_const_requirement_error(self):
        source = '''
            struct X {};
            struct Y {};
            struct Z {};
    
            Poco::Fruit::Component<Poco::Fruit::Required<const X>, std::function<Y()>, std::function<Z()>> getRootComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<Y(const X&)>([](const X&) { return Y();})
                .registerFactory<Z(X&)>([](X&) { return Z();});
            }
            '''
        expect_compile_error(
            'ConstBindingDeclaredAsRequiredButNonConstBindingRequiredError<X>',
            'The type T was declared as a const Required type in the returned Component, however',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_provider_get_error_type_unique_pointer_pointer_not_provided(self):
        source = '''
            struct X {};
    
            void f(Poco::Fruit::Provider<X> provider) {
              provider.get<std::unique_ptr<X>*>();
            }
            '''
        expect_compile_error(
            r'TypeNotProvidedError<std::unique_ptr<X(,std::default_delete<X>)?>\*>',
            r'Trying to get an instance of T, but it is not provided by this Provider/Injector.',
            COMMON_DEFINITIONS,
            source)

    @multiple_parameters([
        ('X()', 'X'),
        ('std::unique_ptr<X>(new X())', 'std::unique_ptr<X>'),
    ], [
        'X',
        'std::unique_ptr<X>',
    ], [
        ('Y**', r'Y\*\*'),
        ('std::shared_ptr<Y>*', r'std::shared_ptr<Y>\*'),
        ('std::nullptr_t', r'(std::)?nullptr(_t)?'),
        ('Y*&', r'Y\*&'),
        ('Y(*)()', r'Y(\((__cdecl)?\*\))?\((void)?\)'),
        ('Poco::Fruit::Annotated<Annotation1, Y**>', r'Y\*\*'),
    ])
    def test_register_factory_with_param_error_type_not_injectable(self,
            ConstructX, XPtr, XFactoryResult, YVariant, YVariantRegex):
        source = '''
            struct Y {};
            struct X {};
            
            Poco::Fruit::Component<> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<XPtr(YVariant)>([](YVariant){ return ConstructX; });
            }
            '''
        expect_compile_error(
            'NonInjectableTypeError<YVariantRegex>',
            'The type T is not injectable.',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_bind_nonconst_unique_ptr_factory_to_const_value_factory(self):
        source = '''
            struct X {
              INJECT(X()) = default;
            };
        
            Poco::Fruit::Component<const std::function<X()>> getChildComponent() {
              return Poco::Fruit::createComponent();
            }
            
            Poco::Fruit::Component<std::function<std::unique_ptr<X>()>> getRootComponent() {
              return Poco::Fruit::createComponent()
                  .install(getChildComponent);
            }
            
            int main() {
              Poco::Fruit::Injector<std::function<std::unique_ptr<X>()>> injector(getRootComponent);
              std::function<std::unique_ptr<X>()> xFactory(injector);
              xFactory();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_bind_const_interface_factory_to_nonconst_implementation_factory(self):
        source = '''
            struct X {
              virtual void foo() = 0;
              virtual ~X() = default;
            };
            
            struct Y : public X {
              INJECT(Y()) = default;
    
              void foo() override {
              }
            };
        
            Poco::Fruit::Component<std::function<std::unique_ptr<Y>()>> getChildComponent() {
              return Poco::Fruit::createComponent();
            }
            
            Poco::Fruit::Component<const std::function<std::unique_ptr<X>()>> getRootComponent() {
              return Poco::Fruit::createComponent()
                  .install(getChildComponent)
                  .bind<X, Y>();
            }
            
            int main() {
              Poco::Fruit::Injector<const std::function<std::unique_ptr<X>()>> injector(getRootComponent);
              std::function<std::unique_ptr<X>()> xFactory(injector);
              xFactory();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_register_factory_bind_nonconst_interface_factory_to_const_implementation_factory(self):
        source = '''
            struct X {
              virtual void foo() = 0;
              virtual ~X() = default;
            };
            
            struct Y : public X {
              INJECT(Y()) = default;
              
              void foo() override {
              }
            };
        
            Poco::Fruit::Component<const std::function<std::unique_ptr<Y>()>> getChildComponent() {
              return Poco::Fruit::createComponent();
            }
            
            Poco::Fruit::Component<std::function<std::unique_ptr<X>()>> getRootComponent() {
              return Poco::Fruit::createComponent()
                  .install(getChildComponent)
                  .bind<X, Y>();
            }
            
            int main() {
              Poco::Fruit::Injector<std::function<std::unique_ptr<X>()>> injector(getRootComponent);
              std::function<std::unique_ptr<X>()> xFactory(injector);
              xFactory();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'WithNoAnnotation',
        'WithAnnotation1',
    ])
    def test_register_factory_abstract_class_ok(self, WithAnnot):
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
    
            Poco::Fruit::Component<WithAnnot<std::function<std::unique_ptr<I>()>>> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<WithAnnot<std::unique_ptr<I>>()>([](){return std::unique_ptr<I>(static_cast<I*>(new X()));});
            }
    
            int main() {
              Poco::Fruit::Injector<WithAnnot<std::function<std::unique_ptr<I>()>>> injector(getComponent);
    
              Assert(injector.get<WithAnnot<std::function<std::unique_ptr<I>()>>>()()->foo() == 5);
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        'WithNoAnnotation',
        'WithAnnotation1',
    ])
    def test_register_factory_abstract_class_with_no_virtual_destructor_error(self, WithAnnot):
        if re.search('MSVC', CXX_COMPILER_NAME):
            # This is disabled in MSVC because it compiles cleanly with the latest MSVC.
            # TODO: investigate why this doesn't fail to compile with MSVC and then re-enable it for MSVC too.
            return
        source = '''
            struct I {
              virtual int foo() = 0;
            };
            
            struct X : public I {
              int foo() override {
                return 5;
              }
            };
    
            Poco::Fruit::Component<WithAnnot<std::function<std::unique_ptr<I>()>>> getComponent() {
              return Poco::Fruit::createComponent()
                .registerFactory<WithAnnot<std::unique_ptr<I>>()>([](){return std::unique_ptr<I>(static_cast<I*>(new X()));});
            }
            '''
        expect_compile_error(
            r'RegisterFactoryForUniquePtrOfAbstractClassWithNoVirtualDestructorError<I>',
            r'registerFactory\(\) was called with a lambda that returns a std::unique_ptr<T>, but T is an abstract class',
            COMMON_DEFINITIONS,
            source,
            locals(),
            ignore_warnings=True,
            disable_error_line_number_check=True)

if __name__ == '__main__':
    absltest.main()
