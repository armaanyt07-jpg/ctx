#!/bin/bash
# ContextDrop installer — makes `ctx` available globally

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CTX_FILE="$SCRIPT_DIR/ctx"

echo ""
echo "  ContextDrop installer"
echo "  ─────────────────────"

# Make executable
chmod +x "$CTX_FILE"

# Try to install to a directory on PATH
INSTALL_DIR=""

if [[ -d "$HOME/.local/bin" ]]; then
    INSTALL_DIR="$HOME/.local/bin"
elif [[ -d "/usr/local/bin" ]] && [[ -w "/usr/local/bin" ]]; then
    INSTALL_DIR="/usr/local/bin"
else
    mkdir -p "$HOME/.local/bin"
    INSTALL_DIR="$HOME/.local/bin"
fi

ln -sf "$CTX_FILE" "$INSTALL_DIR/ctx"
echo "  ✓ Linked ctx → $INSTALL_DIR/ctx"

# Check if install dir is on PATH
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    SHELL_RC=""
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        SHELL_RC="$HOME/.bashrc"
    fi

    if [[ -n "$SHELL_RC" ]]; then
        echo "" >> "$SHELL_RC"
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$SHELL_RC"
        echo "  ✓ Added $INSTALL_DIR to PATH in $SHELL_RC"
        echo ""
        echo "  Run: source $SHELL_RC"
        echo "  Then: ctx --help"
    else
        echo "  ! Add this to your shell config:"
        echo "    export PATH=\"$INSTALL_DIR:\$PATH\""
    fi
else
    echo "  ✓ $INSTALL_DIR already on PATH"
    echo ""
    echo "  Ready! Run: ctx --help"
fi

echo ""
