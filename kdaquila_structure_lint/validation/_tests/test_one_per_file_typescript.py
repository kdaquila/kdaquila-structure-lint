"""Tests for one-per-file validation with TypeScript files."""

from pathlib import Path

from kdaquila_structure_lint.test_fixtures import create_minimal_config, create_python_file
from kdaquila_structure_lint.validation._functions.validator_one_per_file import (
    validate_one_per_file,
)


class TestTypeScriptFunctionsFolder:
    """Tests for TypeScript files in _functions folder."""

    def test_single_named_function_passes(self, tmp_path: Path) -> None:
        """Should pass when TypeScript file has single named function."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_functions").mkdir(parents=True)

        content = """export function calculateSum(a: number, b: number): number {
    return a + b;
}
"""
        create_python_file(tmp_path, "src/_functions/calculateSum.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_single_arrow_function_passes(self, tmp_path: Path) -> None:
        """Should pass when TypeScript file has single arrow function."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_functions").mkdir(parents=True)

        content = """export const formatDate = (date: Date): string => {
    return date.toISOString();
};
"""
        create_python_file(tmp_path, "src/_functions/formatDate.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_multiple_functions_fails(self, tmp_path: Path) -> None:
        """Should fail when TypeScript file has multiple functions."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_functions").mkdir(parents=True)

        content = """export function add(a: number, b: number): number {
    return a + b;
}

export function subtract(a: number, b: number): number {
    return a - b;
}
"""
        create_python_file(tmp_path, "src/_functions/math.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1

    def test_types_not_counted(self, tmp_path: Path) -> None:
        """Should not count interfaces, types, or enums as definitions."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_functions").mkdir(parents=True)

        content = """interface UserInput {
    name: string;
    email: string;
}

type UserResponse = {
    id: number;
    user: UserInput;
};

enum Status {
    Active = 'active',
    Inactive = 'inactive'
}

export function processUser(input: UserInput): UserResponse {
    return { id: 1, user: input };
}
"""
        create_python_file(tmp_path, "src/_functions/processUser.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0


class TestTypeScriptClassesFolder:
    """Tests for TypeScript files in _classes folder."""

    def test_single_class_passes(self, tmp_path: Path) -> None:
        """Should pass when TypeScript file has single class."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_classes").mkdir(parents=True)

        content = """export class UserService {
    private users: string[] = [];

    addUser(name: string): void {
        this.users.push(name);
    }

    getUsers(): string[] {
        return this.users;
    }
}
"""
        create_python_file(tmp_path, "src/_classes/UserService.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_multiple_classes_fails(self, tmp_path: Path) -> None:
        """Should fail when TypeScript file has multiple classes."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_classes").mkdir(parents=True)

        content = """export class UserService {
    getUser(): string {
        return 'user';
    }
}

export class ProductService {
    getProduct(): string {
        return 'product';
    }
}
"""
        create_python_file(tmp_path, "src/_classes/services.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1


class TestTypeScriptComponentsFolder:
    """Tests for TypeScript files in _components folder."""

    def test_single_component_passes(self, tmp_path: Path) -> None:
        """Should pass when TSX file has single component."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_components").mkdir(parents=True)

        content = """import React from 'react';

interface ButtonProps {
    label: string;
    onClick: () => void;
}

export const Button = ({ label, onClick }: ButtonProps) => {
    return <button onClick={onClick}>{label}</button>;
};
"""
        create_python_file(tmp_path, "src/_components/Button.tsx", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_multiple_components_fails(self, tmp_path: Path) -> None:
        """Should fail when TSX file has multiple components."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_components").mkdir(parents=True)

        content = """import React from 'react';

export const Header = () => {
    return <header>Header</header>;
};

export const Footer = () => {
    return <footer>Footer</footer>;
};
"""
        create_python_file(tmp_path, "src/_components/layout.tsx", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1


class TestTypeScriptHooksFolder:
    """Tests for TypeScript files in _hooks folder."""

    def test_single_hook_passes(self, tmp_path: Path) -> None:
        """Should pass when TypeScript file has single hook."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_hooks").mkdir(parents=True)

        content = """import { useState, useCallback } from 'react';

export const useCounter = (initialValue: number = 0) => {
    const [count, setCount] = useState(initialValue);

    const increment = useCallback(() => {
        setCount(c => c + 1);
    }, []);

    return { count, increment };
};
"""
        create_python_file(tmp_path, "src/_hooks/useCounter.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_multiple_hooks_fails(self, tmp_path: Path) -> None:
        """Should fail when TypeScript file has multiple hooks."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_hooks").mkdir(parents=True)

        content = """import { useState } from 'react';

export const useCounter = () => {
    const [count, setCount] = useState(0);
    return { count, setCount };
};

export const useToggle = () => {
    const [value, setValue] = useState(false);
    return { value, toggle: () => setValue(v => !v) };
};
"""
        create_python_file(tmp_path, "src/_hooks/hooks.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 1


class TestTypeScriptTypesFolder:
    """Tests for TypeScript files in _types folder."""

    def test_types_folder_not_validated(self, tmp_path: Path) -> None:
        """Should not validate _types folder (allows any number of definitions)."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_types").mkdir(parents=True)

        # Multiple type definitions and even functions should be allowed in _types
        content = """export interface User {
    id: number;
    name: string;
}

export interface Product {
    id: number;
    price: number;
}

export type UserId = number;
export type ProductId = string;

export function isUser(obj: unknown): obj is User {
    return typeof obj === 'object' && obj !== null && 'id' in obj && 'name' in obj;
}

export function isProduct(obj: unknown): obj is Product {
    return typeof obj === 'object' && obj !== null && 'id' in obj && 'price' in obj;
}
"""
        create_python_file(tmp_path, "src/_types/models.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0


class TestTypeScriptExclusions:
    """Tests for TypeScript file exclusions."""

    def test_declaration_files_excluded(self, tmp_path: Path) -> None:
        """Should exclude .d.ts declaration files from validation."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_functions").mkdir(parents=True)

        # Declaration files can have multiple declarations
        content = """declare function functionOne(): void;
declare function functionTwo(): void;
declare class ClassOne {}
declare class ClassTwo {}
"""
        create_python_file(tmp_path, "src/_functions/types.d.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0

    def test_files_outside_standard_folders_not_validated(self, tmp_path: Path) -> None:
        """Should not validate TypeScript files outside standard folders."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "utils").mkdir(parents=True)

        # Multiple functions in non-standard folder should be allowed
        content = """export function helper1(): void {
    console.log('helper1');
}

export function helper2(): void {
    console.log('helper2');
}
"""
        create_python_file(tmp_path, "src/utils/helpers.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0


class TestTypeScriptEdgeCases:
    """Tests for TypeScript edge cases."""

    def test_let_var_assignments_not_counted(self, tmp_path: Path) -> None:
        """Should not count let/var function assignments as definitions."""
        config = create_minimal_config(tmp_path)
        (config.project_root / "src" / "_functions").mkdir(parents=True)

        content = """// let and var assignments should not be counted
let mutableFunction = () => {
    return 'mutable';
};

var oldStyleFunction = function() {
    return 'old style';
};

// Only this const should be counted
export const mainFunction = (): string => {
    return 'main';
};
"""
        create_python_file(tmp_path, "src/_functions/main.ts", content)

        exit_code = validate_one_per_file(config)
        assert exit_code == 0
