import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Random Any",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "Random Any") {
            const origOnConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info, _) {
                const input_name = "any_";

                const any = this.inputs
                    .filter(input => input.name.startsWith(input_name));

                // Remove last unused inputs (skipping any_1)
                while (
                    (any.length > 1)
                    && (any.at(-1).link == null)
                ) {
                    any.pop();
                    this.removeInput(this.inputs.length - 1);
                }

                // Add new 'any' inputs if necessary
                if (any.at(-1)?.link != null) {
                    const slot_id = any.length + 1;
                    this.addInput(`${input_name}${slot_id}`, "*", { optional: true });
                }

                return origOnConnectionsChange?.apply(this, arguments);
            };
        }
    },
});
