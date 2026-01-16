/**
 * Single custom hook - should PASS validation.
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
    // Simplified implementation
    let storedValue = initialValue;
    const setValue = (value: T) => {
        storedValue = value;
        console.log(`Setting ${key} to ${value}`);
    };
    return [storedValue, setValue];
}
