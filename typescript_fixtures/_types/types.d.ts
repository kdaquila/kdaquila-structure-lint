/**
 * Declaration file - should be EXCLUDED from validation entirely.
 */
declare module 'my-library' {
    export function doSomething(): void;
    export function doSomethingElse(): void;
    export class MyClass {}
}
