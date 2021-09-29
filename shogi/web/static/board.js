const SVG_PIECE_DEF_IDS = [null,
	"black-pawn", "black-silver", 
	"black-bishop","black-rook",
	"black-gold","black-king",
	"black-pro-pawn", "black-pro-silver",
	"black-horse", "black-dragon", null, null, null, null, null, null,
	"white-pawn", "white-silver",
	"white-bishop", "white-rook",
	"white-gold","white-king",
	"white-pro-pawn", "white-pro-silver",
	"white-horse", "white-dragon"
];
const NUMBER_JAPANESE_KANJI_SYMBOLS = [ null, "一", "二", "三", "四", "五", "六", "七", "八", "九", "十" ];
const HAND_PIECE_JAPANESE_SYMBOLS = [
	"歩", "銀",
	"角", "飛",
	"金"
];
const USI_HAND_PIECES = { "歩":"P", "銀":"S", "角":"B", "飛":"R", "金":"G" };

const BLACK = 0;
const WHITE = 1;

const Empty = 0;
const Promoted = 6;
const BPawn = 1;
// const BLance = 2;
// const BKnight = 3;
const BSilver = 2;
const BBishop = 3;
const BRook = 4;
const BGold = 5;
const BKing = 6;
const BProPawn = 7;
// const BProLance = 10;
// const BProKnight = 11;
const BProSilver = 8;
const BHorse = 9;
const BDragon = 10;
const WPawn = 17;
// const WLance = 18;
// const WKnight = 19;
const WSilver = 18;
const WBishop = 19;
const WRook = 20;
const WGold = 21;
const WKing = 22;
const WProPawn = 23;
// const WProLance = 26;
// const WProKnight = 27;
const WProSilver = 24;
const WHorse = 25;
const WDragon = 26;

const HPawn = 0;
// const HLance = 1;
// const HKnight = 2;
const HSilver = 1;
const HBishop = 2;
const HRook = 3;
const HGold = 4;

const PieceTypeToHandPieceTable = [null, HPawn, HSilver, HBishop, HRook, HGold, null, HPawn, HSilver, HBishop, HRook, HGold];
const UsiRankChar = ['a', 'b', 'c', 'd', 'e'];

function to_usi(file, rank) {
	return String(file + 1) + UsiRankChar[rank];
}

class Board {
	constructor() {
		this.board = new Array(25);
		this.pieces_in_hand = [new Array(6), new Array(6)];
		this.move_number = 0;
		this.lastmove = null;
		this.reset();
	}

	reset() {
		this.board.fill(Empty);
		this.board[0] = WKing;
		this.board[1] = WPawn;
		this.board[4] = BRook;
		this.board[5] = WGold;
		this.board[9] = BBishop;
		this.board[10] = WSilver;
		this.board[14] = BSilver;
		this.board[15] = WBishop;
		this.board[19] = BGold;
		this.board[20] = WRook;
		this.board[23] = BPawn;
		this.board[24] = BKing;

		this.pieces_in_hand[0].fill(0);
		this.pieces_in_hand[1].fill(0);

		this.move_number = 0;
		this.lastmove = null;
	}

	move(m) {                                             // CAPTUREPIECETYPE(2**4)    PIECETYPE(2**4)     PRROMOTE(2/2**2)    FROM(25/2**5)   TO(25/2**5    if under than 25, it's from hand)
		const to_sq = m & 0b11111;
		const from_sq = (m >> 5) & 0b11111;

		if (from_sq < 25) {
			const promote = (m >> 10) & 0b1;
			const pieceType = (m >> 12) & 0b1111;
			const capturePieceType = (m >> 16) & 0b1111;

			this.board[from_sq] = Empty;
			this.board[to_sq] = pieceType + 16 * (this.move_number % 2) + Promoted * promote;
			if (capturePieceType > 0) {
				this.pieces_in_hand[this.move_number % 2][PieceTypeToHandPieceTable[capturePieceType]]++;
			}
		}
		else {
			const pt = from_sq - 24;
			this.board[to_sq] = pt + 16 * (this.move_number % 2);
			this.pieces_in_hand[this.move_number % 2][PieceTypeToHandPieceTable[pt]]--;
		}
		this.move_number++;
		this.lastmove = m;
	}


	to_svg(scale, mirror=false) {
		const width = 230;
		const height = 192;

		let svg = `<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" width="${width * scale}" height="${height * scale}" viewBox="0 0 ${width} ${height}"${mirror ? ' transform="rotate(180)"' : ''}><defs><g id="black-pawn"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#27497;</text></g><g id="black-silver"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#37504;</text></g><g id="black-gold"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#37329;</text></g><g id="black-bishop"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#35282;</text></g><g id="black-rook"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#39131;</text></g><g id="black-king"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#29579;</text></g><g id="black-pro-pawn"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#12392;</text></g><g id="black-pro-silver" transform="scale(1.0, 0.5)"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="18">&#25104;</text><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="34">&#37504;</text></g><g id="black-horse"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#39340;</text></g><g id="black-dragon"><text font-family="serif" font-size="17" text-anchor="middle" x="10.5" y="16.5">&#40845;</text></g><g id="white-pawn" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#27497;</text></g><g id="white-silver" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#37504;</text></g><g id="white-gold" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#37329;</text></g><g id="white-bishop" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#35282;</text></g><g id="white-rook" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#39131;</text></g><g id="white-king" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#29579;</text></g><g id="white-pro-pawn" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#12392;</text></g><g id="white-pro-silver" transform="scale(1.0, 0.5) rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-22">&#25104;</text><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-6">&#37504;</text></g><g id="white-horse" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#39340;</text></g><g id="white-dragon" transform="rotate(180)"><text font-family="serif" font-size="17" text-anchor="middle" x="-10.5" y="-3.5">&#40845;</text></g></defs>`;
	
		if (this.lastmove != null) {
			const to_sq = this.lastmove & 0b11111;
			const from_sq = (this.lastmove >> 5) & 0b11111;
			const i = Math.floor(to_sq / 5);
			const j = to_sq % 5;
			svg += `<rect x="${20.5 + (4 - i) * 20}" y="${10.5 + j * 20}" width="20" height="20" fill="#f6b94d" />`;
			if (from_sq < 25) {
				const i = Math.floor(from_sq / 5);
				const j = from_sq % 5;
				svg += `<rect x="${20.5 + (5 - i) * 20}" y="${10.5 + j * 20}" width="20" height="20" fill="#fdf0e3" />`;
			}
		}

		svg += '<g stroke="black"><rect x="20" y="10" width="100.5" height="100.5" fill="none" stroke-width="1.5" /><line x1="20.5" y1="30.5" x2="120.5" y2="30.5" stroke-width="1.0" /><line x1="20.5" y1="50.5" x2="120.5" y2="50.5" stroke-width="1.0" /><line x1="20.5" y1="70.5" x2="120.5" y2="70.5" stroke-width="1.0" /><line x1="20.5" y1="90.5" x2="120.5" y2="90.5" stroke-width="1.0" /><line x1="40.5" y1="10.5" x2="40.5" y2="110.5" stroke-width="1.0" /><line x1="60.5" y1="10.5" x2="60.5" y2="110.5" stroke-width="1.0" /><line x1="80.5" y1="10.5" x2="80.5" y2="110.5" stroke-width="1.0" /><line x1="100.5" y1="10.5" x2="100.5" y2="110.5" stroke-width="1.0" /><line x1="120.5" y1="10.5" x2="120.5" y2="110.5" stroke-width="1.0" /></g>';
        svg += '<g><text font-family="serif" text-anchor="middle" font-size="9" x="30.5" y="8">5</text><text font-family="serif" text-anchor="middle" font-size="9" x="50.5" y="8">4</text><text font-family="serif" text-anchor="middle" font-size="9" x="70.5" y="8">3</text><text font-family="serif" text-anchor="middle" font-size="9" x="90.5" y="8">2</text><text font-family="serif" text-anchor="middle" font-size="9" x="110.5" y="8">1</text><text font-family="serif" font-size="9" x="123.5" y="23">一</text><text font-family="serif" font-size="9" x="123.5" y="43">二</text><text font-family="serif" font-size="9" x="123.5" y="63">三</text><text font-family="serif" font-size="9" x="123.5" y="83">四</text><text font-family="serif" font-size="9" x="123.5" y="103">五</text></g>';

		for (let sq = 0; sq < 25; sq++) {
			const pc = this.board[sq];
			const i = Math.floor(sq / 5);
			const j = sq % 5;
			const x = 20.5 + (4 - i) * 20;
			const y = 10.5 + j * 20;
			if (pc != Empty) {
				svg += `<use id="${to_usi(i, j)}" xlink:href="#${SVG_PIECE_DEF_IDS[pc]}" x="${x}" y="${y}" />`;
			} else {
				svg += `<rect id="${to_usi(i, j)}" x="${x}" y="${y}" width="20" height="20" style="fill-opacity: 0;" />`;
			}
		}

		let hand_pieces = [[], []];
		for (let c = 0; c < 2; c++) {
			let i = 0;
			for (let hp = 0; hp < 6; hp++) {
                //TODO
				let n = this.pieces_in_hand[c][hp];
				if (n >= 11) {
					hand_pieces[c].push([i, NUMBER_JAPANESE_KANJI_SYMBOLS[n % 10]]);
					i++;
					hand_pieces[c].push([i, NUMBER_JAPANESE_KANJI_SYMBOLS[10]]);
					i++;
				} else if (n >= 2) {
					hand_pieces[c].push([i, NUMBER_JAPANESE_KANJI_SYMBOLS[n]]);
					i++;
				}
				if (n >= 1) {
					hand_pieces[c].push([i, HAND_PIECE_JAPANESE_SYMBOLS[hp]]);
					i++;
				}
			}
			i++;
			hand_pieces[c].push([i, "手"]);
			i++;
			hand_pieces[c].push([i, c == BLACK ? "先" : "後"]);
			i++;
			hand_pieces[c].push([i, c == BLACK ? "☗" : "☖"]);
		}

		for (let c = 0; c < 2; c++) {
			const x = c == BLACK ? 140 : -16;
			const y = c == BLACK ? 118 : -10;
			const color_text = c == BLACK ? "black" : "white";
			let scale = 1;
			if (hand_pieces[c].length + 1 > 13)
				scale = 13.0 / (hand_pieces[c].length + 1);
			for (let k = 0; k < hand_pieces[c].length; k++) {
				const i = hand_pieces[c][k][0];
				const text = hand_pieces[c][k][1];
				let id = "";
				if (text in USI_HAND_PIECES)
					id = ' id="' + color_text + '-' + USI_HAND_PIECES[text] + '"';
				svg += `<text${id} font-family="serif" font-size="${14 * scale}" x="${x}" y="${y - 14 * scale * i}"${c == WHITE ? ' transform="rotate(180)"' : ''}>${text}</text>`;
			}
		}

		return svg;
	}
}