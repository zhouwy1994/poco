#include <Poco/Fruit/fruit.h>

struct X {
  INJECT(X()) = default;
};

Poco::Fruit::Component<X> getXComponent() {
  return Poco::Fruit::createComponent();
}

int main() {
  Poco::Fruit::Injector<X> injector(getXComponent);
  injector.get<X*>();
}
