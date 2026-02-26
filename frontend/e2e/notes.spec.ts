import { test, expect } from '@playwright/test';

test('create note via UI', async ({ page }) => {
    await page.goto('/');

    const title = `Nota E2E ${Date.now()}`;
    const content = 'Contenuto E2E';

    await page.getByTestId('create-note-title').fill(title);
    await page.getByTestId('create-note-content').fill(content);
    await page.getByTestId('create-note-submit').click();

    await expect(page.getByTestId('notes-list').getByText(title)).toBeVisible();
});