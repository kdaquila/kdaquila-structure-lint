/**
 * Single class - should PASS validation.
 */
export class UserService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    async getUser(id: number): Promise<void> {
        console.log(`Getting user ${id} from ${this.apiUrl}`);
    }
}
