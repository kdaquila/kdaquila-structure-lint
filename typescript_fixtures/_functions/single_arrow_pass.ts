/**
 * Single arrow function - should PASS validation.
 */
export const fetchUser = async (id: number): Promise<void> => {
    console.log(`Fetching user ${id}`);
};

// Interfaces don't count as definitions
interface User {
    id: number;
    name: string;
}
