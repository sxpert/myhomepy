using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet
{
    public class ProductVersion
    {
        public int Version { get; internal set; }
        public int Release { get; internal set; }
        public int Build { get; internal set; }

        public ProductVersion(int version, int release, int build)
        {
            CheckArgumentValue(version, "Version must be greater than 0");
            CheckArgumentValue(release, "Release must be greater than 0");
            CheckArgumentValue(build, "Build must be greater than 0");

            this.Version = version;
            this.Release = release;
            this.Build = build;
        }

        public override string ToString()
        {
            return string.Format("{0}.{1}.{2}", Version, Release, Build);
        }

        private void CheckArgumentValue(int value, string message)
        {
            if (value < 0)
                throw new ArgumentOutOfRangeException(message);
        }
    }
}
