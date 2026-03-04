#!/bin/bash
# Maven Class Analyzer - Test Script
# Tests the maven-class-analyzer skill with commons-lang3:3.12.0

set -e

echo "=================================="
echo "Maven Class Analyzer - Test Suite"
echo "=================================="

# Test Configuration
GROUP_ID="org.apache.commons"
ARTIFACT_ID="commons-lang3"
VERSION="3.12.0"
TARGET_CLASS="StringUtils"

echo ""
echo "Target Dependency:"
echo "  groupId: $GROUP_ID"
echo "  artifactId: $ARTIFACT_ID"
echo "  version: $VERSION"
echo "  class: $TARGET_CLASS"
echo ""

# Step 1: Create temp directory
WORK_DIR="/tmp/maven_class_analyzer_test"
echo "[Step 1] Creating work directory: $WORK_DIR"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Step 2: Create POM
echo "[Step 2] Creating pom.xml..."
cat > pom.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>temp</groupId>
    <artifactId>analyzer</artifactId>
    <version>1.0</version>
    <dependencies>
        <dependency>
            <groupId>${GROUP_ID}</groupId>
            <artifactId>${ARTIFACT_ID}</artifactId>
            <version>${VERSION}</version>
        </dependency>
    </dependencies>
</project>
EOF
echo "✓ pom.xml created"

# Step 3: Download dependencies
echo "[Step 3] Downloading dependencies..."
mvn dependency:copy-dependencies -DoutputDirectory=./lib -DincludeScope=compile -q
echo "✓ Dependencies downloaded to ./lib/"

# Step 4: List downloaded JARs
echo ""
echo "[Step 4] Downloaded JARs:"
ls -lh lib/*.jar | awk '{print "  " $9 " (" $5 ")"}'

# Step 5: Find target class
echo ""
echo "[Step 5] Finding ${TARGET_CLASS} in JARs..."
JAR_FILE=$(find lib -name "*.jar" -exec sh -c 'unzip -l "$1" 2>/dev/null | grep -qi "'"${TARGET_CLASS}"'.class" && echo "$1"' _ {} \; | head -1)

if [ -z "$JAR_FILE" ]; then
    echo "✗ Class not found!"
    exit 1
fi

echo "✓ Found in: $(basename $JAR_FILE)"

# Step 6: List all matching classes
echo ""
echo "[Step 6] All ${TARGET_CLASS} classes in JAR:"
unzip -l "$JAR_FILE" 2>/dev/null | grep -i "${TARGET_CLASS}.class" | awk '{print "  " $4}'

# Step 7: Analyze main class
echo ""
echo "[Step 7] Analyzing org.apache.commons.lang3.${TARGET_CLASS}..."
echo "=========================================="

# Get class basic info
echo ""
echo "Class Info:"
javap -classpath "$JAR_FILE" org.apache.commons.lang3.${TARGET_CLASS} | head -10

# Get field list
echo ""
echo "Public Fields (first 10):"
javap -classpath "$JAR_FILE" -p org.apache.commons.lang3.${TARGET_CLASS} | grep "public static final" | head -10

# Get method list
echo ""
echo "Public Methods (first 15):"
javap -classpath "$JAR_FILE" org.apache.commons.lang3.${TARGET_CLASS} | grep "public static" | grep -v "final" | head -15

# Step 8: Analyze specific method with signature
echo ""
echo "[Step 8] Analyzing isEmpty() method with signature..."
echo "=========================================="
javap -classpath "$JAR_FILE" -p -s org.apache.commons.lang3.${TARGET_CLASS} | grep -A 2 "isEmpty"

# Step 9: Analyze method with parameters
echo ""
echo "[Step 9] Analyzing abbreviate() method overloads..."
echo "=========================================="
javap -classpath "$JAR_FILE" -s org.apache.commons.lang3.${TARGET_CLASS} | grep -A 1 "abbreviate"

# Summary
echo ""
echo "=================================="
echo "Test completed successfully!"
echo "=================================="
echo ""
echo "Skills verified:"
echo "  ✓ Create temporary POM"
echo "  ✓ Download Maven dependencies"
echo "  ✓ Find class in JARs"
echo "  ✓ List class members"
echo "  ✓ Show method signatures"
echo "  ✓ Extract parameter types"
echo ""
echo "Work directory: $WORK_DIR"
echo "(Clean up manually if needed: rm -rf $WORK_DIR)"
