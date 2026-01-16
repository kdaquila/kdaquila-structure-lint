/**
 * Single React component - should PASS validation.
 */
interface ButtonProps {
    label: string;
    onClick: () => void;
}

export const Button = ({ label, onClick }: ButtonProps) => {
    return <button onClick={onClick}>{label}</button>;
};
