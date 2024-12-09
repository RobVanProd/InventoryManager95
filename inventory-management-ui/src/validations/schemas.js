import * as Yup from 'yup';

export const inventoryItemSchema = Yup.object().shape({
  name: Yup.string()
    .required('Item name is required')
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must not exceed 100 characters'),
  quantity: Yup.number()
    .required('Quantity is required')
    .min(0, 'Quantity cannot be negative')
    .integer('Quantity must be a whole number'),
  description: Yup.string()
    .max(500, 'Description must not exceed 500 characters'),
  price: Yup.number()
    .min(0, 'Price cannot be negative')
    .transform((value) => (isNaN(value) ? undefined : value))
    .nullable(),
  warehouse: Yup.number().nullable(),
  subwarehouse: Yup.number().nullable(),
});
