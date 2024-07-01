/*
 * Copyright 2014 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "cached_greeter.h"
#include "fake_key_value_storage.h"

#include <gtest/gtest.h>

Fruit::Component<Fruit::Annotated<Cached, Greeter>> getMainComponent() {
  return Fruit::createComponent()
      // Note: order matters here. This replace().with() must be before the install. Otherwise Fruit will report the
      // wrong order as a run-time error.
      .replace(getKeyValueStorageComponent).with(getFakeKeyValueStorageComponent)
      .install(getCachedGreeterComponent);
}

Fruit::Component<> getEmptyComponent() {
  return Fruit::createComponent();
}

Fruit::Injector<Fruit::Annotated<Cached, Greeter>> createInjector() {
  static Fruit::NormalizedComponent<Fruit::Annotated<Cached, Greeter>> normalizedComponent(getMainComponent);
  return Fruit::Injector<Fruit::Annotated<Cached, Greeter>>(normalizedComponent, getEmptyComponent);
}

TEST(CachedGreeter, NotYetCached) {
  Fruit::Injector<Fruit::Annotated<Cached, Greeter>> injector = createInjector();
  Greeter* greeter = injector.get<Fruit::Annotated<Cached, Greeter*>>();
  ASSERT_EQ(greeter->greet(), "Hello, world!");
}

TEST(CachedGreeter, Cached) {
  Fruit::Injector<Fruit::Annotated<Cached, Greeter>> injector = createInjector();
  Greeter* greeter = injector.get<Fruit::Annotated<Cached, Greeter*>>();
  greeter->greet();
  ASSERT_EQ(greeter->greet(), "Hello, world!");
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
