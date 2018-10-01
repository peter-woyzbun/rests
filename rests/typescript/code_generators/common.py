from rests.core.typescript.code_generator import CodeGenerator


# =================================
# Common Code Generators
# ---------------------------------

# Accessibility
public = CodeGenerator("public")
private = CodeGenerator("private")
protected = CodeGenerator("protected")


# Static
static = CodeGenerator("static")

# Async/await
async_ = CodeGenerator("async")
await = CodeGenerator("await")

# Get/set
get = CodeGenerator("get")
set_ = CodeGenerator("set")

# Export
export = CodeGenerator("export")
