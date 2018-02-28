/**
 * 
 */
package tape;

/**
 * @author William Bradley
 *
 */
public class Node {
	protected char content;
	protected Node next;
	protected Node prev;
	
	public Node (char ch) {
		content = ch;
		next = null;
		prev = null;
	}
	public Node (char ch, Node n, Node p) {
		content = ch;
		next = n;
		prev = p;
	}
	/* Function to set link to next node */
	public void setLinkNext(Node n) {
		next = n;
	}
	/* Function to set link to prev node */
	public void setLinkPrev(Node p) {
		prev = p;
	}
	/* Function to get link for next node */
	public Node getLinkNext() {
		return next;
	}
	/* Function to get link for prev node */
	public Node getLinkPrev() {
		return prev;
	}
	/* Function to set content at node */
	public void setContent(char ch) {
		content = ch;
	}
	/* Function to get content at node */
	public char getContent() {
		return content;
	}
}
