/**
 * Not in a standard folder - should be SKIPPED (no validation).
 */
export function foo(): void {
    console.log('foo');
}

export function bar(): void {
    console.log('bar');
}

export class Baz {
    baz(): void {
        console.log('baz');
    }
}
