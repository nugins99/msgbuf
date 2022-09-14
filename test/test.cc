#include "oarchive.hpp"
#include "iarchive.hpp"
#include "A.hpp"
#include <iostream>



int main()
{
    oarchive oa;
    A a;
    a.a(42);
    a.b(11);
    a.c("Hello world");
    oa << a;

    // Reverse the process
    iarchive ia(oa.stream.str());
    A b;
    ia >> b;

    std::cout << b.c() << std::endl;

    if (a == b)
    {
        std::cout << "a == b" << std::endl;
    }
    else
    {
        std::cout << "a != b" <<  std::endl;
    }

    return 0;
};