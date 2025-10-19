import { z } from "zod";

export function field<T>(schema: z.ZodSchema<T>, valueToValidate: T) {
  try {
    schema.parse(valueToValidate);
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errorMessage: string = error?.issues?.[0]?.message
        ? error?.issues?.[0]?.message
        : "";

      return {
        isValid: false,
        error: errorMessage
      };
    }
  }

  return {
    isValid: true,
    error: ""
  };
}
