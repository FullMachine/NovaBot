import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export const defaultAvatar = 'https://api.dicebear.com/7.x/bottts/svg?seed=DefaultPlayer&backgroundColor=blue';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getSafeImage(src: string | undefined, fallback: string = defaultAvatar) {
  return src && src.trim() !== '' ? src : fallback;
}

export function slugify(name: string): string {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
