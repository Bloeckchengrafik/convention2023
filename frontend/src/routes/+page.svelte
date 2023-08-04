<script>
    import Empty from "$lib/Empty.svelte";
</script>

<div class="h-full row gap-3">
    <div class="column">
        <div class="card h-full">
            <div class="card-header">
                <h1>Overview</h1>
            </div>
            <div class="card-body">
                <p>To start the program, create a new pipeline first.</p>
            </div>
        </div>
    </div>
    <div class="column">
        <div class="card h-full">
            <div class="card-header">
                <h1>Last Runs</h1>
            </div>
            <div class="card-body">
                <Empty />
            </div>
        </div>
    </div>
</div>