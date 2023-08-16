#pragma once
#include <type_traits>

/// hton(s,l,ll), ntoh(s,l,ll) template functions.
// The calling function is not type-aware, and we don't have a generic overload for hton or ntoh functions
// so we preovide specialized versions of each.
namespace serialization
{

    template <typename T, std::enable_if_t<sizeof(T) == 8, bool> = true>
    T hton(T value)
    {
#if defined(__BYTE_ORDER__) && (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
        return value;
#else
        auto integral_value = reinterpret_cast<uint64_t*>(&value);
        return ((((uint64_t)htonl(*integral_value)) << 32) + htonl((*integral_value) >> 32));
#endif
    }

    template <typename T, std::enable_if_t<sizeof(T) == 4, bool> = true> 
    T hton(T value)
    {
        return htonl(value);
    }

    template <typename T, std::enable_if_t<sizeof(T) == 2, bool> = true>
    T hton(T value)
    {
        return ntohs(value);
    }

    template <typename T, std::enable_if_t<sizeof(T) == 8, bool> = true>
    T ntoh(T value)
    {
#if defined(__BYTE_ORDER__) && (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
        return value;
#else
        return ((((uint64_t)ntohl(value)) << 32) + ntohl((value) >> 32));
#endif
    }
    template <typename T, std::enable_if_t<sizeof(T) == 4, bool> = true> 
    T ntoh(T value)
    {
        return ntohl(value);
    }

    template <typename T, std::enable_if_t<sizeof(T) == 2, bool> = true>
    T ntoh(T value)
    {
        return ntohl(value);
    }
}
