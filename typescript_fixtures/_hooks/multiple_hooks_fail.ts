/**
 * Multiple hooks - should FAIL validation.
 */
export function useToggle(initial: boolean = false): [boolean, () => void] {
    let value = initial;
    return [value, () => { value = !value; }];
}

export function useCounter(initial: number = 0): [number, () => void] {
    let count = initial;
    return [count, () => { count++; }];
}
