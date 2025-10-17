export function numberString(value: string): string {
  return value.toString().replace(/[^0-9]/g, "");
}
