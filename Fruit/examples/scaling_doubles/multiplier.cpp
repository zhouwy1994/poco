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

#include "multiplier.h"

class MultiplierImpl : public Multiplier {
public:
  double multiply(double x, double y) override {
    return x * y;
  }
};

Poco::Fruit::Component<Multiplier> getMultiplierComponent() {
  return Poco::Fruit::createComponent().bind<Multiplier, MultiplierImpl>().registerConstructor<MultiplierImpl()>();
}
