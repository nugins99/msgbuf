#include <sstream>
#include "byteswap.hpp"

class oarchive
{
    public:

    template <typename T>
    oarchive & operator<<(T & t)
    {
        t.serialize(*this);
        return *this;
    }

    template <typename T>
    void write(const T & value)
    {
        // TODO - account for network byte order
        const auto value_swapped = serialization::hton(value);
        stream.write((const char *)&value_swapped, sizeof(T));
    }

    std::ostringstream stream;
};

template<>
void oarchive::write(const std::string & value)
{
    uint16_t len = value.size();
    write(len);
    stream.write(value.data(), len);
}


template <typename T>
void operator&(oarchive & oa, T value)
{
    oa.write(value);
}