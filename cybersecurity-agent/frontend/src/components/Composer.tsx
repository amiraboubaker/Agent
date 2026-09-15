import { ArrowUp, Paperclip } from "lucide-react";
import { useState } from "react";

export function Composer({ onSend, disabled }: { onSend: (message: string) => void; disabled: boolean }) {
    const [value, setValue] = useState("");
    function submit() { if (value.trim() && !disabled) { onSend(value.trim()); setValue(""); } }
    return <div className="composer-wrap"><div className="composer"><textarea value={value} onChange={(event) => setValue(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); submit(); } }} placeholder="Ask the Cybersecurity Agent for defensive guidance..." rows={2} /><div className="composer-actions"><button className="icon-button" type="button" title="Attachments"><Paperclip size={18} /></button><span className="composer-hint">Enter to send · Shift + Enter for a new line</span><button className="send-button" disabled={disabled || !value.trim()} onClick={submit} type="button"><ArrowUp size={19} /></button></div></div><p className="safety-note">Only assess systems you own or are explicitly authorized to test. Never share credentials or secrets.</p></div>;
}
