package tape;

public class Main {

	public static void main(String[] args) {
		DoublyLinkedList tape = new DoublyLinkedList();
		Node runner = tape.head;
		String msg = "World";
		for (int i = 0; i < msg.length(); i++) {
			runner.setContent(msg.charAt(i));
			// create a new node to the right of the old node
			tape.nodeRight('>', runner);
			runner = runner.getLinkNext();
		}
		for (int i = 0; i < "Hello World".length(); i++) {
			if (runner.getLinkPrev() != null) {
				runner = runner.getLinkPrev();
			}
			else {
				tape.nodeLeft('<', runner);
				runner = runner.getLinkPrev();
				tape.head = runner;
			}
		}
		msg = "Hello";
		for (int i = 0; i < msg.length(); i++) {
			runner.setContent(msg.charAt(i));
			runner = runner.getLinkNext();
		}
		runner = tape.head;
		printLinkedList(runner, false);
	}
	public static void printLinkedList(Node runner, boolean debug) {
		while (runner.getLinkNext() != null) {
			if (debug == true) {
				System.out.print("Node: " + runner + " ---->\t" + "Next: " + runner.getLinkNext());
				System.out.print(" ---->\tPrev: " + runner.getLinkPrev());
				System.out.print(" ---->\tCONTENT: " + runner.getContent() + "\n");
			}
			else {
				System.out.print(runner.getContent());
			}
			runner = runner.getLinkNext();
		}
	}
}
