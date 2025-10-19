export function int(value: string): string {
    const stringValue = String(value);
    if (!stringValue.trim()) return "0";
    return parseInt(stringValue, 10).toString();
}