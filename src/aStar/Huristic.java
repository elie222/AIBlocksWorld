package aStar;

public interface Huristic<N extends Node<N>> {
	public double getHur(N node1, N node2);
}
