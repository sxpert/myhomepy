using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;

namespace OpenWebNet
{
    public class StringValueAttribute : Attribute
    {
        private static Dictionary<Enum, StringValueAttribute> _values;

        static StringValueAttribute()
        {
            _values = new Dictionary<Enum, StringValueAttribute>();
        }

        public StringValueAttribute(String value)
            : base()
        {
            Value = value;
        }

        public String Value { get; private set; }

        public static String GetStringValue(Enum value)
        {
            String output = null;
            Type type = value.GetType();

            //Check first in our cached results...

            if (_values.ContainsKey(value))
            {
                output = _values[value].Value;
            }
            else
            {
                //Look for our 'StringValueAttribute' 

                //in the field's custom attributes

                FieldInfo fi = type.GetField(value.ToString());
                StringValueAttribute[] attrs =
                   fi.GetCustomAttributes(typeof(StringValueAttribute),
                                           false) as StringValueAttribute[];
                if (attrs.Length > 0)
                {
                    _values.Add(value, attrs[0]);
                    output = attrs[0].Value;
                }
            }

            return output;
        }
    }
}
