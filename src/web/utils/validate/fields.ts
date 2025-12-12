import { z } from "zod";

interface ValidationError {
  [key: string]: string;
}

// This is a generic function that receives a schema and a value and returns
export function fields<T>(schema: z.ZodSchema<Partial<T>>, value: T) {
  try {
    schema.parse(value);
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors: ValidationError = {};

      error.issues.forEach((error) => {
        errors[error.path[0]] = error.message;
      });

      return {
        isValid: false,
        errors
      };
    }
  }

  return { isValid: true, errors: null };
}
