import type { PageLoad } from '../../../../../.svelte-kit/types/src/routes'
export const load = (async ({params}) => {
    return {
        id: params.id,
    }
}) satisfies PageLoad