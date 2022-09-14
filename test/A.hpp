#include <string>

/// Description for message A
class A
{
    public:
    
    /// Getter for a
    int a() const { return m_a; }
    /// Setter for a
    A & a(int value) { m_a = value; return *this; }
    
    /// Getter for b
    float b() const { return m_b; }
    /// Setter for b
    A & b(float value) { m_b = value; return *this; }
    
    /// Getter for c
    std::string c() const { return m_c; }
    /// Setter for c
    A & c(std::string value) { m_c = value; return *this; }
    
    /// Getter for d
    double d() const { return m_d; }
    /// Setter for d
    A & d(double value) { m_d = value; return *this; }
    

    /// This function provides both serialization and deserialization.
    /// This is influenced by the boost serialization library.
    template <typename Archive> void serialize(Archive & archive)
    {
        archive & m_a; 
        archive & m_b; 
        archive & m_c; 
        archive & m_d; 
    }

    
    bool operator==(const A & rhs) const
    {
        if (m_a != rhs.m_a) return false;
        if (m_b != rhs.m_b) return false;
        if (m_c != rhs.m_c) return false;
        if (m_d != rhs.m_d) return false;
        return true;
    }

    bool operator!=(const A & rhs) const
    {
        return !(*this==rhs);
    }

    private:
     
    /// An int type
    int m_a;
     
    /// A float type
    float m_b;
     
    /// A string type
    std::string m_c;
     
    /// A double type
    double m_d;
    
};