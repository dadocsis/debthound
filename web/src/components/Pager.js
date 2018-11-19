import React from "react";

const PREV_NEXT_COUNT = 2;

class Pager extends React.Component {
    constructor(props){
        super(props);
        this.pageClick.bind(this);
    }

    pageClick(page){
        this.props.handlePageClick(page);
    }

    render(){
        let trailingPages = [];
        let leadingPages = [];
        let step = this.props.currentPage - PREV_NEXT_COUNT;
        let key = 0;

        for (let i=step; i < this.props.currentPage; i++){
            if (i<=0) continue;
            key++;
            trailingPages.push((<li className="page-item" key={key}>
                <button className={"page-link"} onClick={() => this.pageClick(step)}>{i}</button></li>))
        }
        //current page
        trailingPages.push((<li className="page-item active" key={key}>
                <button className={"page-link"} onClick={() => this.pageClick(this.props.currentPage)}>
                    {this.props.currentPage}</button></li>))

        for (let i=this.props.currentPage+1; i <= PREV_NEXT_COUNT + this.props.currentPage; i++){
            if (i >= this.props.totalPages) break;
            key++;
            leadingPages.push((<li className="page-item" key={key}>
                <button className="page-link" onClick={() => this.pageClick(i)}>
                    {i}</button></li>))
        }

        let prevPage = this.props.currentPage > 1 ? this.props.currentPage - 1 : 1;
        return (
        <nav aria-label="Page navigation example">
                  <ul className="pagination">
                        <li className="page-item">
                          <button className="page-link" aria-label="Previous"
                                  onClick={() => this.pageClick(prevPage)}>
                            <span aria-hidden="true">&laquo;</span>
                            <span className="sr-only">Previous</span>
                          </button>
                        </li>
                            {[...trailingPages, ...leadingPages]}
                        <li className="page-item">
                      <button className="page-link" aria-label="Next"
                              onClick={() => this.pageClick(this.props.currentPage + 1)}>
                        <span aria-hidden="true">&raquo;</span>
                        <span className="sr-only">Next</span>
                      </button>
                    </li>
                  </ul>
                </nav>)
    }
}
export default Pager