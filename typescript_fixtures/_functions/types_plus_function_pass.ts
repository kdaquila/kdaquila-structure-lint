/**
 * Types don't count - only 1 function, should PASS.
 */
interface InputData {
    value: string;
}

type OutputData = {
    result: string;
};

enum Status {
    Pending,
    Complete
}

export function transform(input: InputData): OutputData {
    return { result: input.value };
}
