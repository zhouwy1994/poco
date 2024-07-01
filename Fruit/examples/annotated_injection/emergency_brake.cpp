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

#include "emergency_brake.h"

class EmergencyBrakeImpl : public Brake {
public:
  INJECT(EmergencyBrakeImpl()) = default;

  void activate() override {
    // ...
  }
};

Poco::Fruit::Component<Poco::Fruit::Annotated<EmergencyBrake, Brake>> getEmergencyBrakeComponent() {
  return Poco::Fruit::createComponent().bind<Poco::Fruit::Annotated<EmergencyBrake, Brake>, EmergencyBrakeImpl>();
}
