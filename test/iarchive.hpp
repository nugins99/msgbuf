#include <sstream>
#include <vector>
#include "byteswap.hpp"

class iarchive
{
    public:
    iarchive(std::string data) : stream(std::move(data)) { }

    template <typename T>
    iarchive & operator>>(T & t)
    {
        t.serialize(*this);
        return *this;
    }

    template <typename T>
    void read(T & value)
    {
        // TODO - account for network byte order
        stream.read((char *)&value, sizeof(T));
        value = serialization::hton(value);
    }

    std::istringstream stream;
};

template<>
void iarchive::read(std::string & value)
{
    uint16_t len = 0;
    read(len);
    std::vector<char> buf(len);
    stream.read(buf.data(), len);
    value = {buf.begin(), buf.end()};
}


template <typename T>
void operator&(iarchive & oa, T & value)
{
    oa.read(value);
}