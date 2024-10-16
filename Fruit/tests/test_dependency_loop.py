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

    struct Annotation2 {};
    using XAnnot2 = Poco::Fruit::Annotated<Annotation2, X>;

    struct Annotation3 {};
    using XAnnot3 = Poco::Fruit::Annotated<Annotation3, X>;
    '''

class TestDependencyLoop(parameterized.TestCase):
    @parameterized.parameters([
        ('X', 'const X&', 'Y', 'const Y&'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'ANNOTATED(Annotation1, const X&)',
         'Poco::Fruit::Annotated<Annotation2, Y>', 'ANNOTATED(Annotation2, const Y&)')
    ])
    def test_loop_in_autoinject(self, XAnnot, XConstRefAnnot, YAnnot, YConstRefAnnot):
        source = '''
            struct Y;
    
            struct X {
              INJECT(X(YConstRefAnnot)) {};
            };
    
            struct Y {
              INJECT(Y(XConstRefAnnot)) {};
            };
    
            Poco::Fruit::Component<XAnnot> mutuallyConstructibleComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'SelfLoopError<XAnnot,YAnnot>',
            'Found a loop in the dependencies',
            COMMON_DEFINITIONS,
            source,
            locals())

    @parameterized.parameters([
        ('X', 'const X', 'const X&', 'Y', 'const Y&'),
        ('Poco::Fruit::Annotated<Annotation1, X>', 'ANNOTATED(Annotation1, const X)', 'ANNOTATED(Annotation1, const X&)',
         'Poco::Fruit::Annotated<Annotation2, Y>', 'ANNOTATED(Annotation2, const Y&)')
    ])
    def test_loop_in_autoinject_const(self, XAnnot, ConstXAnnot, XConstRefAnnot, YAnnot, YConstRefAnnot):
        source = '''
            struct Y;
    
            struct X {
              INJECT(X(YConstRefAnnot)) {};
            };
    
            struct Y {
              INJECT(Y(XConstRefAnnot)) {};
            };
    
            Poco::Fruit::Component<ConstXAnnot> mutuallyConstructibleComponent() {
              return Poco::Fruit::createComponent();
            }
            '''
        expect_compile_error(
            'SelfLoopError<XAnnot,YAnnot>',
            'Found a loop in the dependencies',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_loop_in_register_provider(self):
        source = '''
            struct X {};
            struct Y {};
    
            Poco::Fruit::Component<X> mutuallyConstructibleComponent() {
              return Poco::Fruit::createComponent()
                  .registerProvider<X(Y)>([](Y) {return X();})
                  .registerProvider<Y(X)>([](X) {return Y();});
            }
            '''
        expect_compile_error(
            'SelfLoopError<X,Y>',
            'Found a loop in the dependencies',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_loop_in_register_provider_with_annotations(self):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<Poco::Fruit::Annotated<Annotation1, X>> mutuallyConstructibleComponent() {
              return Poco::Fruit::createComponent()
                  .registerProvider<Poco::Fruit::Annotated<Annotation1, X>(Poco::Fruit::Annotated<Annotation2, X>)>([](X x) {return x;})
                  .registerProvider<Poco::Fruit::Annotated<Annotation2, X>(Poco::Fruit::Annotated<Annotation1, X>)>([](X x) {return x;});
            }
            '''
        expect_compile_error(
            'SelfLoopError<Poco::Fruit::Annotated<Annotation1, X>, Poco::Fruit::Annotated<Annotation2, X>>',
            'Found a loop in the dependencies',
            COMMON_DEFINITIONS,
            source,
            locals())

    def test_with_different_annotations_ok(self):
        source = '''
            struct X {};
    
            Poco::Fruit::Component<XAnnot3> getComponent() {
              return Poco::Fruit::createComponent()
                  .registerProvider<XAnnot1()>([](){return X();})
                  .registerProvider<XAnnot2(XAnnot1)>([](X x){return x;})
                  .registerProvider<XAnnot3(XAnnot2)>([](X x){return x;});
            }
    
            int main() {
              Poco::Fruit::Injector<XAnnot3> injector(getComponent);
              injector.get<XAnnot3>();
            }
            '''
        expect_success(
            COMMON_DEFINITIONS,
            source)

if __name__ == '__main__':
    absltest.main()
