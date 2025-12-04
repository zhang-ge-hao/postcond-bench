https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/utils/helpers.py#L51-L110
```
@icontract.snapshot(
    lambda task, event: [
        (art.artifact_id, list(art.parts)) for art in (task.artifacts or [])
    ],
    name="old_artifacts",
)
@icontract.snapshot(
    lambda task, event: [art.artifact_id for art in (task.artifacts or [])],
    name="old_ids",
)
@icontract.snapshot(
    lambda task, event: {
        art.artifact_id: list(art.parts) for art in (task.artifacts or [])
    },
    name="old_parts_map",
)
@icontract.ensure(
    lambda OLD, task, event:
        isinstance(task.artifacts, list)
        and all(isinstance(art, Artifact) for art in (task.artifacts or []))
        and (
            event.append
            or (
                (
                    event.artifact.artifact_id in OLD.old_ids
                    and len(task.artifacts) == len(OLD.old_ids)
                    and task.artifacts[
                        OLD.old_ids.index(event.artifact.artifact_id)
                    ].artifact_id
                    == event.artifact.artifact_id
                    and [
                        p
                        for p in task.artifacts[
                            OLD.old_ids.index(event.artifact.artifact_id)
                        ].parts
                    ]
                    == [p for p in event.artifact.parts]
                    and all(
                        (j == OLD.old_ids.index(event.artifact.artifact_id))
                        or (
                            task.artifacts[j].artifact_id == OLD.old_ids[j]
                            and [p for p in task.artifacts[j].parts]
                            == OLD.old_parts_map[OLD.old_ids[j]]
                        )
                        for j in range(len(OLD.old_ids))
                    )
                )
                or (
                    event.artifact.artifact_id not in OLD.old_ids
                    and len(task.artifacts) == len(OLD.old_ids) + 1
                    and task.artifacts[-1].artifact_id
                    == event.artifact.artifact_id
                    and [p for p in task.artifacts[-1].parts]
                    == [p for p in event.artifact.parts]
                    and all(
                        task.artifacts[j].artifact_id == OLD.old_ids[j]
                        and [p for p in task.artifacts[j].parts]
                        == OLD.old_parts_map[OLD.old_ids[j]]
                        for j in range(len(OLD.old_ids))
                    )
                )
            )
        )
        and (
            (not event.append)
            or (
                (
                    event.artifact.artifact_id in OLD.old_ids
                    and len(task.artifacts) == len(OLD.old_ids)
                    and task.artifacts[
                        OLD.old_ids.index(event.artifact.artifact_id)
                    ].artifact_id
                    == event.artifact.artifact_id
                    and [
                        p
                        for p in task.artifacts[
                            OLD.old_ids.index(event.artifact.artifact_id)
                        ].parts
                    ]
                    == OLD.old_parts_map[event.artifact.artifact_id]
                    + [p for p in event.artifact.parts]
                    and all(
                        (j == OLD.old_ids.index(event.artifact.artifact_id))
                        or (
                            task.artifacts[j].artifact_id == OLD.old_ids[j]
                            and [p for p in task.artifacts[j].parts]
                            == OLD.old_parts_map[OLD.old_ids[j]]
                        )
                        for j in range(len(OLD.old_ids))
                    )
                )
                or (
                    event.artifact.artifact_id not in OLD.old_ids
                    and len(task.artifacts) == len(OLD.old_ids)
                    and all(
                        task.artifacts[j].artifact_id == OLD.old_ids[j]
                        and [p for p in task.artifacts[j].parts]
                        == OLD.old_parts_map[OLD.old_ids[j]]
                        for j in range(len(OLD.old_ids))
                    )
                )
            )
        )
)
```
```
@icontract.snapshot(lambda task, event: [(art.artifact_id, list(art.parts)) for art in (task.artifacts or [])], name="old_artifacts")
@icontract.snapshot(lambda task, event: [art.artifact_id for art in (task.artifacts or [])], name="old_ids")
@icontract.snapshot(lambda task, event: {art.artifact_id: list(art.parts) for art in (task.artifacts or [])}, name="old_parts_map")
@icontract.ensure(lambda OLD, task, event: isinstance(task.artifacts, list))
@icontract.ensure(lambda OLD, task, event: (event.append) or (
    (
        event.artifact.artifact_id in OLD.old_ids and
        len(task.artifacts) == len(OLD.old_ids) and
        task.artifacts[OLD.old_ids.index(event.artifact.artifact_id)].artifact_id == event.artifact.artifact_id and
        [p for p in task.artifacts[OLD.old_ids.index(event.artifact.artifact_id)].parts] == [p for p in event.artifact.parts] and
        all(
            (j == OLD.old_ids.index(event.artifact.artifact_id)) or
            (
                task.artifacts[j].artifact_id == OLD.old_ids[j] and
                [p for p in task.artifacts[j].parts] == OLD.old_parts_map[OLD.old_ids[j]]
            )
            for j in range(len(OLD.old_ids))
        )
    ) or (
        event.artifact.artifact_id not in OLD.old_ids and
        len(task.artifacts) == len(OLD.old_ids) + 1 and
        task.artifacts[-1].artifact_id == event.artifact.artifact_id and
        [p for p in task.artifacts[-1].parts] == [p for p in event.artifact.parts] and
        all(
            task.artifacts[j].artifact_id == OLD.old_ids[j] and
            [p for p in task.artifacts[j].parts] == OLD.old_parts_map[OLD.old_ids[j]]
            for j in range(len(OLD.old_ids))
        )
    )
))
@icontract.ensure(lambda OLD, task, event: (not event.append) or (
    (
        event.artifact.artifact_id in OLD.old_ids and
        len(task.artifacts) == len(OLD.old_ids) and
        task.artifacts[OLD.old_ids.index(event.artifact.artifact_id)].artifact_id == event.artifact.artifact_id and
        [p for p in task.artifacts[OLD.old_ids.index(event.artifact.artifact_id)].parts] == OLD.old_parts_map[event.artifact.artifact_id] + [p for p in event.artifact.parts] and
        all(
            (j == OLD.old_ids.index(event.artifact.artifact_id)) or
            (
                task.artifacts[j].artifact_id == OLD.old_ids[j] and
                [p for p in task.artifacts[j].parts] == OLD.old_parts_map[OLD.old_ids[j]]
            )
            for j in range(len(OLD.old_ids))
        )
    ) or (
        event.artifact.artifact_id not in OLD.old_ids and
        len(task.artifacts) == len(OLD.old_ids) and
        all(
            task.artifacts[j].artifact_id == OLD.old_ids[j] and
            [p for p in task.artifacts[j].parts] == OLD.old_parts_map[OLD.old_ids[j]]
            for j in range(len(OLD.old_ids))
        )
    )
))
```
[19, 21]
===== 19 =====
```
             logger.debug(
                 'Replacing artifact at id %s for task %s', artifact_id, task.id
             )
-            task.artifacts[existing_artifact_list_index] = new_artifact_data
+            task.artifacts[existing_artifact_list_index] = None
         else:
             # Append the new artifact since no artifact with this index exists yet
             logger.debug(
@@ -57,4 +57,4 @@             'Received append=True for nonexistent artifact index %s in task %s. Ignoring chunk.',
             artifact_id,
             task.id,
-        )+        )
```
```
@trace_function()
def append_artifact_to_task(task: Task, event: TaskArtifactUpdateEvent) -> None:
    """Helper method for updating a Task object with new artifact data from an event.

    Handles creating the artifacts list if it doesn't exist, adding new artifacts,
    and appending parts to existing artifacts based on the `append` flag in the event.

    Args:
        task: The `Task` object to modify.
        event: The `TaskArtifactUpdateEvent` containing the artifact data.
    """
    if not task.artifacts:
        task.artifacts = []

    new_artifact_data: Artifact = event.artifact
    artifact_id: str = new_artifact_data.artifact_id
    append_parts: bool = event.append or False

    existing_artifact: Artifact | None = None
    existing_artifact_list_index: int | None = None

    # Find existing artifact by its id
    for i, art in enumerate(task.artifacts):
        if art.artifact_id == artifact_id:
            existing_artifact = art
            existing_artifact_list_index = i
            break

    if not append_parts:
        # This represents the first chunk for this artifact index.
        if existing_artifact_list_index is not None:
            # Replace the existing artifact entirely with the new data
            logger.debug(
                'Replacing artifact at id %s for task %s', artifact_id, task.id
            )
            task.artifacts[existing_artifact_list_index] = None
        else:
            # Append the new artifact since no artifact with this index exists yet
            logger.debug(
                'Adding new artifact with id %s for task %s',
                artifact_id,
                task.id,
            )
            task.artifacts.append(new_artifact_data)
    elif existing_artifact:
        # Append new parts to the existing artifact's part list
        logger.debug(
            'Appending parts to artifact id %s for task %s',
            artifact_id,
            task.id,
        )
        existing_artifact.parts.extend(new_artifact_data.parts)
    else:
        # We received a chunk to append, but we don't have an existing artifact.
        # we will ignore this chunk
        logger.warning(
            'Received append=True for nonexistent artifact index %s in task %s. Ignoring chunk.',
            artifact_id,
            task.id,
        )

```
===== 21 =====
```
                 artifact_id,
                 task.id,
             )
-            task.artifacts.append(new_artifact_data)
+            task.artifacts.append(None)
     elif existing_artifact:
         # Append new parts to the existing artifact's part list
         logger.debug(
@@ -57,4 +57,4 @@             'Received append=True for nonexistent artifact index %s in task %s. Ignoring chunk.',
             artifact_id,
             task.id,
-        )+        )
```
```
@trace_function()
def append_artifact_to_task(task: Task, event: TaskArtifactUpdateEvent) -> None:
    """Helper method for updating a Task object with new artifact data from an event.

    Handles creating the artifacts list if it doesn't exist, adding new artifacts,
    and appending parts to existing artifacts based on the `append` flag in the event.

    Args:
        task: The `Task` object to modify.
        event: The `TaskArtifactUpdateEvent` containing the artifact data.
    """
    if not task.artifacts:
        task.artifacts = []

    new_artifact_data: Artifact = event.artifact
    artifact_id: str = new_artifact_data.artifact_id
    append_parts: bool = event.append or False

    existing_artifact: Artifact | None = None
    existing_artifact_list_index: int | None = None

    # Find existing artifact by its id
    for i, art in enumerate(task.artifacts):
        if art.artifact_id == artifact_id:
            existing_artifact = art
            existing_artifact_list_index = i
            break

    if not append_parts:
        # This represents the first chunk for this artifact index.
        if existing_artifact_list_index is not None:
            # Replace the existing artifact entirely with the new data
            logger.debug(
                'Replacing artifact at id %s for task %s', artifact_id, task.id
            )
            task.artifacts[existing_artifact_list_index] = new_artifact_data
        else:
            # Append the new artifact since no artifact with this index exists yet
            logger.debug(
                'Adding new artifact with id %s for task %s',
                artifact_id,
                task.id,
            )
            task.artifacts.append(None)
    elif existing_artifact:
        # Append new parts to the existing artifact's part list
        logger.debug(
            'Appending parts to artifact id %s for task %s',
            artifact_id,
            task.id,
        )
        existing_artifact.parts.extend(new_artifact_data.parts)
    else:
        # We received a chunk to append, but we don't have an existing artifact.
        # we will ignore this chunk
        logger.warning(
            'Received append=True for nonexistent artifact index %s in task %s. Ignoring chunk.',
            artifact_id,
            task.id,
        )

```
