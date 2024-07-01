#include <Poco/Fruit/fruit.h>

struct X {
  INJECT(X()) = default;
};

Fruit::Component<X> getXComponent() {
  return Fruit::createComponent();
}

int main() {
  Fruit::Injector<X> injector(getXComponent);
  injector.get<X*>();
}
