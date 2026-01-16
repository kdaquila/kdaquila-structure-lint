/**
 * Multiple types - _types folder has NO validation rule, should PASS.
 */
export interface User {
    id: number;
    name: string;
}

export interface Post {
    id: number;
    title: string;
}

export type UserId = number;
export type PostId = number;

// Even functions are allowed in _types (no validation)
export function createUser(name: string): User {
    return { id: 1, name };
}

export function createPost(title: string): Post {
    return { id: 1, title };
}
