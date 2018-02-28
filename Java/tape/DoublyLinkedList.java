/**
 * 
 */
package tape;

/**
 * @author William Bradley
 *
 */
public class DoublyLinkedList {
	protected Node head;
	protected Node tail;
	public DoublyLinkedList() {
		Node node = new Node(' ');
		this.head = node;
		this.tail = node;
	}
	public Node nodeRight(char ch, Node current) {
		Node node = new Node(' ');
		current.setLinkNext(node);
		node.setLinkPrev(current);
		return node;
	}
	public Node nodeLeft(char ch, Node current) {
		Node node = new Node(' ');
		current.setLinkPrev(node);
		node.setLinkNext(current);
		return node;
	}
}
