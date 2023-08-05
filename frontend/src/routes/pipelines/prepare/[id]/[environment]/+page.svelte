<script lang="ts">
    import type {PageData} from "./$types";

    export let data: PageData;
</script>

<h1>hello #{data.id} ({data.env})</h1>
